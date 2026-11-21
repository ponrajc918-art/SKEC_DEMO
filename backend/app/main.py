from __future__ import annotations
from datetime import datetime,timedelta
import json,re,secrets
from fastapi import Depends,FastAPI,HTTPException,Request,Response,status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import IntegrityError
from .core import SessionLocal,allowed_origins,engine,get_db,hash_otp,hash_password,hash_token,is_expired,new_token,now,password_policy_error,settings,validate_production_settings,verify_password
from .models import (Assignment,AssignmentSubmission,AttendanceRecord,AttendanceSession,Base,Circular,Department,EmailDelivery,Enquiry,FileObject,Invitation,Invoice,LeaveRequest,LoginAttempt,MfaFactor,MfaRecoveryCode,Notification,PasswordHistory,PasswordResetToken,Payment,PaymentGatewayEvent,Result,Role,SessionRecord,Staff,Student,SubjectOffering,TimetableEntry,User,UserRole,VerificationChallenge)
from .schemas import AdminStudentIn,AssignmentIn,AttendanceIn,CircularIn,EnquiryIn,InvitationAcceptIn,LeaveRequestIn,LoginIn,MfaVerifyIn,MobileVerificationRequestIn,OtpVerifyIn,PasswordChangeIn,PasswordResetConfirmIn,PasswordResetRequestIn,PaymentOrderIn,PaymentVerifyIn,ProfileIn,ResultIn,SubmissionIn
from .security import audit,create_session,current_user,password_was_used,remember_replaced_password,require_permission,require_csrf,roles
from .seed import seed
from .email_service import deliver
from .payment_service import create_order,enabled as razorpay_enabled,verify_payment_signature,verify_webhook
from .storage_service import private_path,save_private
from .mfa_service import decrypt as decrypt_mfa,encrypt as encrypt_mfa,new_secret,otpauth_uri,verify as verify_totp
from .scanner_service import ScannerUnavailable,scan as scan_file
from .sms_service import SmsUnavailable,send_otp
app=FastAPI(title="SKEC Digital Campus API",version="1.0.0",openapi_url="/api/v1/openapi.json",docs_url="/api/docs")
app.add_middleware(CORSMiddleware,allow_origins=allowed_origins(),allow_credentials=True,allow_methods=["GET","POST","PATCH"],allow_headers=["Content-Type","X-CSRF-Token"])
@app.middleware("http")
async def security_headers(request:Request,call_next):
    response=await call_next(request)
    response.headers["X-Content-Type-Options"]="nosniff";response.headers["X-Frame-Options"]="DENY";response.headers["Referrer-Policy"]="strict-origin-when-cross-origin";response.headers["Permissions-Policy"]="camera=(), microphone=(), geolocation=()"
    if settings().app_env=="production":response.headers["Strict-Transport-Security"]="max-age=31536000; includeSubDomains"
    return response
@app.on_event("startup")
def start():
    validate_production_settings()
    if settings().app_env == "development":
        Base.metadata.create_all(bind=engine)
        db=SessionLocal()
        try: seed(db)
        finally: db.close()
@app.get("/api/v1/health")
def health():return {"status":"ok","service":"skec-campus-api"}

MOBILE_PATTERN=re.compile(r"^\+91[6-9]\d{9}$")
def client_ip(request:Request)->str:return request.client.host if request.client else "unknown"
def new_otp()->str:return f"{secrets.randbelow(1_000_000):06d}"
def current_student_or_forbidden(db:Session,user:User)->Student:
    student=db.query(Student).filter_by(user_id=user.id).first()
    if not student:raise HTTPException(status_code=403,detail={"code":"scope_violation","message":"Student record required"})
    return student
def current_staff_or_forbidden(db:Session,user:User)->Staff:
    staff=db.query(Staff).filter_by(user_id=user.id).first()
    if not staff:raise HTTPException(status_code=403,detail={"code":"scope_violation","message":"Staff record required"})
    return staff
def replace_password_or_raise(db:Session,user:User,password:str)->None:
    policy_error=password_policy_error(password)
    if policy_error:raise HTTPException(status_code=422,detail={"code":"weak_password","message":policy_error})
    if password_was_used(db,user,password):raise HTTPException(status_code=422,detail={"code":"password_reused","message":"Choose a password that has not been used recently"})
    remember_replaced_password(db,user);user.password_hash=hash_password(password)
def issue_verification_challenge(db:Session,user:User,destination:str,channel:str,purpose:str,request:Request)->str:
    cfg=settings();current=now();ip=client_ip(request)
    latest=db.query(VerificationChallenge).filter_by(user_id=user.id,destination=destination,channel=channel,purpose=purpose,consumed_at=None).order_by(VerificationChallenge.created_at.desc()).first()
    if latest and (current-latest.created_at.replace(tzinfo=current.tzinfo) if latest.created_at.tzinfo is None else current-latest.created_at).total_seconds()<cfg.otp_resend_cooldown_seconds:
        raise HTTPException(status_code=429,detail={"code":"otp_cooldown","message":"Please wait before requesting another verification code"})
    recent=db.query(VerificationChallenge).filter(VerificationChallenge.destination==destination,VerificationChallenge.requested_ip==ip,VerificationChallenge.created_at>=current-timedelta(minutes=15)).count()
    if recent>=3:raise HTTPException(status_code=429,detail={"code":"otp_rate_limited","message":"Too many verification requests"})
    db.query(VerificationChallenge).filter_by(user_id=user.id,destination=destination,channel=channel,purpose=purpose,consumed_at=None).update({VerificationChallenge.consumed_at:current})
    code=new_otp();db.add(VerificationChallenge(user_id=user.id,destination=destination,channel=channel,purpose=purpose,otp_hash=hash_otp(code),requested_ip=ip,expires_at=current+timedelta(minutes=cfg.otp_expiry_minutes)))
    return code
def verify_challenge(db:Session,user:User,channel:str,purpose:str,code:str)->VerificationChallenge|None:
    row=db.query(VerificationChallenge).filter_by(user_id=user.id,channel=channel,purpose=purpose,consumed_at=None).order_by(VerificationChallenge.created_at.desc()).with_for_update().first()
    if not row or is_expired(row.expires_at) or row.attempts>=settings().otp_max_attempts:return None
    row.attempts+=1
    if not secrets.compare_digest(row.otp_hash,hash_otp(code)):return None
    row.consumed_at=now()
    return row
@app.post("/api/v1/auth/login")
def login(payload:LoginIn,response:Response,request:Request,db:Session=Depends(get_db)):
    identifier=payload.email.lower();ip=request.client.host if request.client else "unknown";window=now()-timedelta(minutes=15)
    identifier_failures=db.query(LoginAttempt).filter(LoginAttempt.identifier==identifier,LoginAttempt.success.is_(False),LoginAttempt.attempted_at>=window).count()
    ip_failures=db.query(LoginAttempt).filter(LoginAttempt.ip==ip,LoginAttempt.success.is_(False),LoginAttempt.attempted_at>=window).count()
    if identifier_failures>=5 or ip_failures>=20:raise HTTPException(status_code=429,detail={"code":"too_many_attempts","message":"Please wait before trying again"})
    user=db.query(User).filter(User.email==identifier).first();valid=bool(user and user.status=="active" and verify_password(payload.password,user.password_hash));mfa_enrollment_required=False
    required_roles={role.strip() for role in settings().mfa_required_roles.split(",") if role.strip()}
    if valid and settings().app_env=="production" and roles(user).intersection(required_roles):
        factor=db.query(MfaFactor).filter_by(user_id=user.id).first()
        if factor and factor.confirmed_at:
            valid=bool(payload.mfa_code and verify_totp(decrypt_mfa(factor.secret_encrypted),payload.mfa_code))
            if not valid and payload.mfa_recovery_code:
                recovery=db.query(MfaRecoveryCode).filter_by(user_id=user.id,code_hash=hash_token(payload.mfa_recovery_code),used_at=None).with_for_update().first()
                if recovery:
                    recovery.used_at=now();valid=True;audit(db,user.id,"mfa.recovery_code_used","user",user.id)
        else:
            # A newly provisioned privileged account needs one authenticated session to
            # enrol its authenticator; deployment runbooks require completing this before use.
            mfa_enrollment_required=True
    db.add(LoginAttempt(identifier=identifier,ip=ip,success=valid))
    if not valid:
        audit(db,None,"auth.login_failed","user",None,{"identifier":identifier});db.commit();raise HTTPException(status_code=401,detail={"code":"invalid_credentials","message":"Invalid credentials"})
    user.last_login_at=now();token,csrf=create_session(db,user);secure=settings().app_env=="production";response.set_cookie(settings().session_cookie_name,token,httponly=True,secure=secure,samesite="lax",max_age=43200,path="/");response.set_cookie("skec_csrf",csrf,httponly=False,secure=secure,samesite="lax",max_age=43200,path="/");return {"message":"signed_in","csrf_token":csrf,"must_change_password":user.must_change_password,"mfa_enrollment_required":mfa_enrollment_required}
@app.post("/api/v1/auth/mfa/enroll")
def enroll_mfa(user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if not roles(user).intersection(set(filter(None,settings().mfa_required_roles.split(",")))):raise HTTPException(status_code=403,detail={"code":"forbidden","message":"MFA enrolment is reserved for privileged roles"})
    secret=new_secret();factor=db.query(MfaFactor).filter_by(user_id=user.id).first()
    if factor:factor.secret_encrypted=encrypt_mfa(secret);factor.confirmed_at=None
    else:db.add(MfaFactor(user_id=user.id,secret_encrypted=encrypt_mfa(secret)))
    audit(db,user.id,"mfa.enrolment_started","user",user.id);db.commit();return {"otpauth_uri":otpauth_uri(secret,user.email),"notice":"Add this URI to an authenticator application, then confirm a six-digit code."}
@app.post("/api/v1/auth/mfa/confirm")
def confirm_mfa(payload:MfaVerifyIn,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    factor=db.query(MfaFactor).filter_by(user_id=user.id).first()
    if not factor or not verify_totp(decrypt_mfa(factor.secret_encrypted),payload.code):raise HTTPException(status_code=400,detail={"code":"invalid_mfa_code","message":"Authenticator code is invalid"})
    factor.confirmed_at=now();audit(db,user.id,"mfa.enabled","user",user.id);db.commit();return {"message":"mfa_enabled"}
@app.post("/api/v1/auth/mfa/recovery-codes")
def generate_mfa_recovery_codes(user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    factor=db.query(MfaFactor).filter_by(user_id=user.id).first()
    if not factor or not factor.confirmed_at:raise HTTPException(status_code=400,detail={"code":"mfa_not_enabled","message":"Enable MFA before generating recovery codes"})
    db.query(MfaRecoveryCode).filter_by(user_id=user.id,used_at=None).update({MfaRecoveryCode.used_at:now()})
    codes=[secrets.token_urlsafe(9) for _ in range(10)]
    db.add_all(MfaRecoveryCode(user_id=user.id,code_hash=hash_token(code)) for code in codes)
    audit(db,user.id,"mfa.recovery_codes_generated","user",user.id,{"count":len(codes)});db.commit()
    return {"recovery_codes":codes,"notice":"Store these one-time recovery codes securely. They will not be shown again."}
@app.post("/api/v1/auth/email-verification/request")
def request_email_verification(request:Request,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    code=issue_verification_challenge(db,user,user.email,"email","email_verification",request)
    delivery=deliver(db,user.email,"email_otp",user.id,code=code,expires_minutes=settings().otp_expiry_minutes)
    if delivery not in {"sent","mocked"}:db.rollback();raise HTTPException(status_code=503,detail={"code":"email_unavailable","message":"Email verification is currently unavailable"})
    audit(db,user.id,"email.verification_requested","user",user.id);db.commit();return {"message":"If delivery is available, a verification code was sent."}
@app.post("/api/v1/auth/email-verification/confirm")
def confirm_email_verification(payload:OtpVerifyIn,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    challenge=verify_challenge(db,user,"email","email_verification",payload.code)
    if not challenge or challenge.destination!=user.email:
        db.commit()
        raise HTTPException(status_code=400,detail={"code":"invalid_otp","message":"Verification code is invalid or expired"})
    user.email_verified_at=now()
    audit(db,user.id,"email.verified","user",user.id)
    db.commit()
    return {"message":"email_verified"}
@app.post("/api/v1/auth/mobile-verification/request")
def request_mobile_verification(payload:MobileVerificationRequestIn,request:Request,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if not MOBILE_PATTERN.fullmatch(payload.mobile_number):
        raise HTTPException(status_code=422,detail={"code":"invalid_mobile","message":"Use an Indian mobile number in +91XXXXXXXXXX format"})
    existing=db.query(User).filter(User.mobile_number==payload.mobile_number,User.id!=user.id).first()
    if existing:
        raise HTTPException(status_code=409,detail={"code":"duplicate_mobile","message":"Mobile number is already registered"})
    code=issue_verification_challenge(db,user,payload.mobile_number,"sms","mobile_verification",request)
    try:
        send_otp(payload.mobile_number,code)
    except SmsUnavailable as exc:
        db.rollback()
        raise HTTPException(status_code=503,detail={"code":"sms_unavailable","message":"SMS verification is not configured or unavailable"}) from exc
    audit(db,user.id,"mobile.verification_requested","user",user.id)
    db.commit()
    return {"message":"A verification code was sent if the SMS provider accepted the request."}


@app.post("/api/v1/auth/mobile-verification/confirm")
def confirm_mobile_verification(payload:OtpVerifyIn,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    challenge=verify_challenge(db,user,"sms","mobile_verification",payload.code)
    if not challenge:
        db.commit()
        raise HTTPException(status_code=400,detail={"code":"invalid_otp","message":"Verification code is invalid or expired"})
    existing=db.query(User).filter(User.mobile_number==challenge.destination,User.id!=user.id).first()
    if existing:
        db.commit()
        raise HTTPException(status_code=409,detail={"code":"duplicate_mobile","message":"Mobile number is already registered"})
    user.mobile_number=challenge.destination
    user.mobile_verified_at=now()
    audit(db,user.id,"mobile.verified","user",user.id)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail={"code":"duplicate_mobile","message":"Mobile number is already registered"})
    return {"message":"mobile_verified"}
@app.post("/api/v1/auth/mobile-verification/confirm")
def confirm_mobile_verification(payload:OtpVerifyIn,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if not verify_challenge(db,user,"sms","mobile_verification",payload.code):db.commit();raise HTTPException(status_code=400,detail={"code":"invalid_otp","message":"Verification code is invalid or expired"})
    user.mobile_verified_at=now();audit(db,user.id,"mobile.verified","user",user.id);db.commit();return {"message":"mobile_verified"}
@app.post("/api/v1/auth/logout")
def logout(request:Request,response:Response,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    raw=request.cookies.get(settings().session_cookie_name);record=db.get(SessionRecord,hash_token(raw or ""));
    if record:record.revoked_at=now();audit(db,user.id,"auth.logout","user",user.id);db.commit()
    response.delete_cookie(settings().session_cookie_name);response.delete_cookie("skec_csrf");return {"message":"signed_out"}
@app.post("/api/v1/auth/sign-out-everywhere")
def sign_out_everywhere(user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    db.query(SessionRecord).filter(SessionRecord.user_id==user.id,SessionRecord.revoked_at.is_(None)).update({SessionRecord.revoked_at:now()});audit(db,user.id,"auth.sign_out_everywhere","user",user.id);db.commit();return {"message":"all_sessions_revoked"}
@app.post("/api/v1/auth/password-reset/request")
def request_password_reset(payload:PasswordResetRequestIn,db:Session=Depends(get_db)):
    user=db.query(User).filter_by(email=payload.email.lower()).first()
    if user and user.status=="active":
        raw=new_token();db.query(PasswordResetToken).filter_by(user_id=user.id,purpose="password_reset",used_at=None).update({PasswordResetToken.used_at:now()})
        db.add(PasswordResetToken(user_id=user.id,token_hash=hash_token(raw),purpose="password_reset",expires_at=now()+timedelta(minutes=30)));link=f"{settings().public_site_url}/portal/reset-password?token={raw}";delivery=deliver(db,user.email,"password_reset",user.id,link=link);audit(db,user.id,"auth.password_reset_requested","user",user.id,{"delivery":delivery});db.commit()
    return {"message":"If the account exists, reset instructions were sent."}
@app.post("/api/v1/auth/password-reset/confirm")
def confirm_password_reset(payload:PasswordResetConfirmIn,db:Session=Depends(get_db)):
    row=db.query(PasswordResetToken).filter_by(token_hash=hash_token(payload.token),purpose="password_reset",used_at=None).first()
    if not row or is_expired(row.expires_at):raise HTTPException(status_code=400,detail={"code":"invalid_token","message":"Reset token is invalid or expired"})
    user=db.get(User,row.user_id);replace_password_or_raise(db,user,payload.new_password);user.must_change_password=False;row.used_at=now();db.query(SessionRecord).filter_by(user_id=user.id,revoked_at=None).update({SessionRecord.revoked_at:now()});delivery=deliver(db,user.email,"password_changed",user.id);audit(db,user.id,"auth.password_reset_completed","user",user.id,{"delivery":delivery});db.commit();return {"message":"password_reset"}
@app.post("/api/v1/auth/password/change")
def change_password(payload:PasswordChangeIn,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if not verify_password(payload.current_password,user.password_hash):raise HTTPException(status_code=400,detail={"code":"invalid_credentials","message":"Current password is incorrect"})
    replace_password_or_raise(db,user,payload.new_password);user.must_change_password=False;db.query(SessionRecord).filter(SessionRecord.user_id==user.id,SessionRecord.revoked_at.is_(None)).update({SessionRecord.revoked_at:now()});delivery=deliver(db,user.email,"password_changed",user.id);audit(db,user.id,"auth.password_changed","user",user.id,{"delivery":delivery});db.commit();return {"message":"password_changed_sign_in_again"}
@app.post("/api/v1/auth/invitations/accept")
def accept_invitation(payload:InvitationAcceptIn,db:Session=Depends(get_db)):
    invite=(
        db.query(Invitation)
        .filter_by(
            token_hash=hash_token(payload.token),
            accepted_at=None
        )
        .with_for_update()
        .first()
    )

    if not invite or is_expired(invite.expires_at):
        raise HTTPException(
            status_code=400,
            detail={
                "code":"invalid_token",
                "message":"Invitation is invalid or expired"
            }
        )

    user=db.get(User,invite.user_id)

    if not user:
        raise HTTPException(
            status_code=400,
            detail={
                "code":"invalid_token",
                "message":"Invitation is invalid or expired"
            }
        )

    current_time=now()
    replace_password_or_raise(db,user,payload.password)
    user.status="active"
    user.must_change_password=False
    user.email_verified_at=current_time
    invite.accepted_at=current_time

    audit(
        db,
        user.id,
        "auth.invitation_accepted",
        "user",
        user.id
    )

    db.commit()

    return {"message":"account_activated"}
@app.get("/api/v1/auth/me")
def me(user:User=Depends(current_user),db:Session=Depends(get_db)):
    u=db.query(User).options(joinedload(User.student).joinedload(Student.department),joinedload(User.staff).joinedload(Staff.department),joinedload(User.roles)).filter(User.id==user.id).one();factor=db.query(MfaFactor).filter_by(user_id=u.id).first();return {"email":u.email,"email_verified":bool(u.email_verified_at),"mobile_number":u.mobile_number,"mobile_verified":bool(u.mobile_verified_at),"mfa_enabled":bool(factor and factor.confirmed_at),"roles":sorted(roles(u)),"student":None if not u.student else {"register_number":u.student.register_number,"programme":u.student.programme},"staff":None if not u.staff else {"employee_id":u.staff.employee_id,"department":u.staff.department.name}}
@app.post("/api/v1/enquiries",status_code=201)
def enquiry(payload:EnquiryIn,db:Session=Depends(get_db)):
    if payload.website:raise HTTPException(status_code=400,detail={"code":"invalid_submission","message":"Invalid form"})
    row=Enquiry(name=payload.name,contact=payload.contact,message=payload.message);db.add(row);audit(db,None,"enquiry.created","enquiry",row.id);db.commit();return {"id":row.id,"status":"saved","notice":"Saved to the development database; no communication was sent."}
@app.get("/api/v1/attendance/mine")
def attendance_mine(user:User=Depends(current_user),db:Session=Depends(get_db)):
    if "student" in roles(user):
        student=db.query(Student).filter_by(user_id=user.id).one();records=db.query(AttendanceRecord).join(AttendanceSession).filter(AttendanceRecord.student_id==student.id).all();return {"records":[{"status":r.status,"subject":r.session.offering.code,"date":r.session.session_date.isoformat()} for r in records]}
    if roles(user).intersection({"staff","hod","principal","college_admin"}):
        rows=db.query(AttendanceSession).order_by(AttendanceSession.session_date.desc()).all();return {"records":[{"status":"Recorded","subject":r.offering.code,"date":r.session_date.isoformat()} for r in rows]}
    raise HTTPException(status_code=403,detail={"code":"forbidden","message":"Academic role required"})
@app.post("/api/v1/attendance",status_code=201)
def mark_attendance(payload:AttendanceIn,user:User=Depends(require_permission("academic.attendance.write")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    staff=current_staff_or_forbidden(db,user);offering=db.get(SubjectOffering,payload.offering_id)
    if not offering or offering.staff_id!=staff.id:raise HTTPException(status_code=403,detail={"code":"scope_violation","message":"Not assigned to this subject"})
    existing=db.query(AttendanceSession).filter_by(offering_id=offering.id,session_date=payload.session_date).first()
    if existing:raise HTTPException(status_code=409,detail={"code":"duplicate_session","message":"Attendance already exists for this date"})
    session=AttendanceSession(offering_id=offering.id,session_date=payload.session_date,marked_by=staff.id);db.add(session);db.flush()
    for item in payload.records:
        student=db.get(Student,item.student_id)
        if not student or student.department_id!=offering.department_id:raise HTTPException(status_code=400,detail={"code":"invalid_student","message":"Student is outside this offering scope"})
        db.add(AttendanceRecord(session_id=session.id,student_id=student.id,status=item.status))
    audit(db,user.id,"attendance.marked","attendance_session",session.id);db.commit();return {"id":session.id,"saved":len(payload.records)}
@app.get("/api/v1/assignments/mine")
def assignments_mine(user:User=Depends(current_user),db:Session=Depends(get_db)):
    if "student" in roles(user):
        student=db.query(Student).filter_by(user_id=user.id).one();items=db.query(Assignment).join(SubjectOffering).filter(SubjectOffering.department_id==student.department_id).all();return {"mode":"student","assignments":[{"id":a.id,"title":a.title,"subject":a.offering.code,"due_at":a.due_at.isoformat(),"max_marks":a.max_marks} for a in items]}
    staff=db.query(Staff).filter_by(user_id=user.id).first()
    if staff:
        items=db.query(Assignment).filter_by(created_by=staff.id).all();return {"mode":"teaching","assignments":[{"id":a.id,"title":a.title,"subject":a.offering.code,"due_at":a.due_at.isoformat(),"max_marks":a.max_marks} for a in items]}
    raise HTTPException(status_code=403,detail={"code":"forbidden","message":"Academic role required"})
@app.post("/api/v1/assignments",status_code=201)
def create_assignment(payload:AssignmentIn,user:User=Depends(require_permission("academic.assignments.write")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    staff=current_staff_or_forbidden(db,user);offering=db.get(SubjectOffering,payload.offering_id)
    if not offering or offering.staff_id!=staff.id:raise HTTPException(status_code=403,detail={"code":"scope_violation","message":"Not assigned to this subject"})
    item=Assignment(**payload.model_dump(),created_by=staff.id);db.add(item);audit(db,user.id,"assignment.created","assignment",item.id);db.commit();return {"id":item.id}
@app.get("/api/v1/results/mine")
def results_mine(user:User=Depends(current_user),db:Session=Depends(get_db)):
    if "student" in roles(user):
        student=db.query(Student).filter_by(user_id=user.id).one();rows=db.query(Result).filter_by(student_id=student.id,status="published").all();return {"results":[{"subject":r.subject_code,"exam":r.exam_name,"marks":r.marks,"grade":r.grade} for r in rows]}
    if roles(user).intersection({"hod","principal","college_admin"}):
        rows=db.query(Result).filter_by(status="published").all();return {"results":[{"subject":r.subject_code,"exam":r.exam_name,"marks":r.marks,"grade":r.grade} for r in rows]}
    raise HTTPException(status_code=403,detail={"code":"forbidden","message":"Result access is not assigned to this account"})
@app.post("/api/v1/results",status_code=201)
def enter_result(payload:ResultIn,user:User=Depends(require_permission("exams.results.write")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    s=db.get(Student,payload.student_id)
    if not s:raise HTTPException(status_code=404,detail={"code":"not_found","message":"Student not found"})
    item=Result(**payload.model_dump(),status="draft");db.add(item);audit(db,user.id,"result.entered","result",item.id);db.commit();return {"id":item.id,"status":"draft"}
@app.post("/api/v1/results/{result_id}/publish")
def publish_result(result_id:str,user:User=Depends(require_permission("exams.results.publish")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    item=db.get(Result,result_id)
    if not item:raise HTTPException(status_code=404,detail={"code":"not_found","message":"Result not found"})
    item.status="published";audit(db,user.id,"result.published","result",item.id);db.commit();return {"id":item.id,"status":"published"}
@app.get("/api/v1/fees/mine")
def fees_mine(user:User=Depends(require_permission("finance.invoices.read_own")),db:Session=Depends(get_db)):
    s=current_student_or_forbidden(db,user);rows=db.query(Invoice).filter_by(student_id=s.id).all();return {"invoices":[{"number":x.number,"amount_inr":x.total_paise/100,"status":x.status,"payment":"Razorpay test adapter not configured"} for x in rows]}
@app.post("/api/v1/circulars",status_code=201)
def create_circular(payload:CircularIn,user:User=Depends(require_permission("announcements.publish")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    item=Circular(**payload.model_dump(),published_by=user.id,status="published");db.add(item);audit(db,user.id,"circular.published","circular",item.id);db.commit();return {"id":item.id,"status":item.status}
@app.get("/api/v1/admin/summary")
def admin_summary(user:User=Depends(require_permission("admin.dashboard.read")),db:Session=Depends(get_db)):return {"students":db.query(Student).count(),"staff":db.query(Staff).count(),"enquiries":db.query(Enquiry).count(),"note":"Counts include clearly labelled demo records in development."}

@app.get("/api/v1/dashboard")
def dashboard(user:User=Depends(current_user),db:Session=Depends(get_db)):
    user_roles=roles(user)
    base={"role":sorted(user_roles)[0],"activities":[],"metrics":[]}
    if "student" in user_roles:
        student=db.query(Student).filter_by(user_id=user.id).one()
        assignments=db.query(Assignment).join(SubjectOffering).filter(SubjectOffering.department_id==student.department_id).count()
        published=db.query(Result).filter_by(student_id=student.id,status="published").count()
        base.update(metrics=[{"label":"Open assignments","value":assignments,"tone":"gold"},{"label":"Published results","value":published,"tone":"navy"},{"label":"Fee status","value":"Due","tone":"rose"}],activities=[{"title":"Your demo workspace is ready","detail":"All visible records are synthetic development data."}])
    elif "staff" in user_roles:
        staff=db.query(Staff).filter_by(user_id=user.id).one(); offerings=db.query(SubjectOffering).filter_by(staff_id=staff.id).count()
        base.update(metrics=[{"label":"Assigned subjects","value":offerings,"tone":"gold"},{"label":"Class roster","value":db.query(Student).filter_by(department_id=staff.department_id).count(),"tone":"navy"},{"label":"Submissions","value":db.query(AssignmentSubmission).count(),"tone":"green"}],activities=[{"title":"Attendance tools available","detail":"Mark attendance only for your assigned subjects."}])
    elif user_roles.intersection({"hod","principal","college_admin"}):
        base.update(metrics=[{"label":"Students","value":db.query(Student).count(),"tone":"navy"},{"label":"Faculty","value":db.query(Staff).count(),"tone":"gold"},{"label":"Open enquiries","value":db.query(Enquiry).filter_by(status="new").count(),"tone":"green"}],activities=[{"title":"Institutional demo overview","detail":"Counts derive from the seeded development database."}])
    return base

@app.get("/api/v1/timetable/mine")
def timetable_mine(user:User=Depends(current_user),db:Session=Depends(get_db)):
    if "student" in roles(user): department_id=db.query(Student).filter_by(user_id=user.id).one().department_id
    else:
        staff=db.query(Staff).filter_by(user_id=user.id).first()
        if not staff: raise HTTPException(status_code=403,detail={"code":"forbidden","message":"No academic timetable scope"})
        department_id=staff.department_id
    rows=db.query(TimetableEntry).join(SubjectOffering).filter(SubjectOffering.department_id==department_id).order_by(TimetableEntry.day_of_week,TimetableEntry.period).all()
    return {"entries":[{"id":r.id,"day":r.day_of_week,"period":r.period,"subject":r.offering.code,"title":r.offering.title,"room":r.room,"time":f"{r.starts_at}–{r.ends_at}"} for r in rows]}

@app.get("/api/v1/teaching/mine")
def teaching_mine(user:User=Depends(require_permission("academic.teaching.read")),db:Session=Depends(get_db)):
    staff=current_staff_or_forbidden(db,user); rows=db.query(SubjectOffering).filter_by(staff_id=staff.id).all()
    roster=db.query(Student).filter_by(department_id=staff.department_id).order_by(Student.full_name).all()
    return {"subjects":[{"id":r.id,"code":r.code,"title":r.title} for r in rows],"students":[{"id":s.id,"name":s.full_name,"register_number":s.register_number} for s in roster]}

@app.get("/api/v1/academic/students")
def academic_students(user:User=Depends(require_permission("academic.students.read")),db:Session=Depends(get_db)):
    if "staff" in roles(user):
        staff=current_staff_or_forbidden(db,user);rows=db.query(Student).filter_by(department_id=staff.department_id).order_by(Student.full_name).all()
    else: rows=db.query(Student).order_by(Student.full_name).all()
    return {"students":[{"id":s.id,"name":s.full_name,"register_number":s.register_number,"programme":s.programme,"department":s.department.code} for s in rows]}

@app.post("/api/v1/assignments/{assignment_id}/submissions",status_code=201)
def submit_assignment(assignment_id:str,payload:SubmissionIn,user:User=Depends(require_permission("student.assignments.submit_own")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    student=current_student_or_forbidden(db,user); assignment=db.get(Assignment,assignment_id)
    if not assignment or assignment.offering.department_id!=student.department_id: raise HTTPException(status_code=404,detail={"code":"not_found","message":"Assignment not found"})
    row=db.query(AssignmentSubmission).filter_by(assignment_id=assignment_id,student_id=student.id).first()
    if row: row.note=payload.note; row.status="resubmitted"
    else: row=AssignmentSubmission(assignment_id=assignment_id,student_id=student.id,note=payload.note); db.add(row)
    audit(db,user.id,"assignment.submitted","assignment",assignment_id);db.commit();return {"id":row.id,"status":row.status}

@app.get("/api/v1/notifications/mine")
def notifications_mine(user:User=Depends(current_user),db:Session=Depends(get_db)):
    rows=db.query(Notification).filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
    return {"notifications":[{"id":r.id,"title":r.title,"body":r.body,"kind":r.kind,"read":bool(r.read_at)} for r in rows]}

@app.get("/api/v1/announcements/mine")
def announcements_mine(user:User=Depends(current_user),db:Session=Depends(get_db)):
    codes=roles(user); rows=db.query(Circular).filter_by(status="published").all()
    return {"announcements":[{"id":r.id,"title":r.title,"body":r.body} for r in rows if not r.audience.get("roles") or codes.intersection(r.audience.get("roles",[]))]}

@app.patch("/api/v1/profile/mine")
def update_profile(payload:ProfileIn,user:User=Depends(current_user),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if "student" in roles(user): target=db.query(Student).filter_by(user_id=user.id).one()
    else:
        target=db.query(Staff).filter_by(user_id=user.id).first()
        if not target: raise HTTPException(status_code=403,detail={"code":"forbidden","message":"No editable profile"})
    target.full_name=payload.full_name;audit(db,user.id,"profile.updated","profile",target.id);db.commit();return {"full_name":target.full_name}

@app.post("/api/v1/leaves",status_code=201)
def create_leave(payload:LeaveRequestIn,user:User=Depends(require_permission("student.leave.create_own")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if payload.to_date<payload.from_date: raise HTTPException(status_code=422,detail={"code":"invalid_dates","message":"End date precedes start date"})
    student=current_student_or_forbidden(db,user);row=LeaveRequest(student_id=student.id,**payload.model_dump());db.add(row);audit(db,user.id,"leave.requested","leave_request",row.id);db.commit();return {"id":row.id,"status":row.status}

@app.get("/api/v1/admin/users")
def admin_users(user:User=Depends(require_permission("admin.users.read")),db:Session=Depends(get_db)):
    rows=db.query(User).options(joinedload(User.roles)).order_by(User.email).all()
    return {"users":[{"id":u.id,"email":u.email,"roles":sorted(roles(u)),"status":u.status} for u in rows]}

@app.post("/api/v1/admin/students",status_code=201)
def admin_create_student(payload:AdminStudentIn,user:User=Depends(require_permission("admin.students.create")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if db.query(User).filter_by(email=payload.email.lower()).first() or db.query(Student).filter_by(register_number=payload.register_number).first(): raise HTTPException(status_code=409,detail={"code":"duplicate","message":"Email or register number exists"})
    if not db.get(Department,payload.department_id): raise HTTPException(status_code=422,detail={"code":"invalid_department","message":"Department not found"})
    policy_error=password_policy_error(payload.password)
    if policy_error:raise HTTPException(status_code=422,detail={"code":"weak_password","message":policy_error})
    account=User(email=payload.email.lower(),password_hash=hash_password(payload.password),must_change_password=True);db.add(account);db.flush();db.add(PasswordHistory(user_id=account.id,password_hash=account.password_hash));role=db.query(Role).filter_by(code="student").one();db.add(UserRole(user_id=account.id,role_id=role.id));student=Student(user_id=account.id,register_number=payload.register_number,full_name=payload.full_name,department_id=payload.department_id,programme=payload.programme);db.add(student);audit(db,user.id,"student.created","student",student.id);db.commit();return {"id":student.id,"email":account.email}
@app.post("/api/v1/admin/users/{user_id}/invite")
def invite_user(user_id:str,user:User=Depends(require_permission("admin.users.invite")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    account=db.get(User,user_id)
    if not account:raise HTTPException(status_code=404,detail={"code":"not_found","message":"User not found"})
    raw=new_token();db.query(Invitation).filter_by(user_id=account.id,accepted_at=None).update({Invitation.accepted_at:now()});invite=Invitation(user_id=account.id,token_hash=hash_token(raw),expires_at=now()+timedelta(days=7),invited_by=user.id);db.add(invite);link=f"{settings().public_site_url}/portal/accept-invitation?token={raw}";delivery=deliver(db,account.email,"invitation",account.id,link=link);audit(db,user.id,"user.invited","user",account.id,{"delivery":delivery});db.commit();return {"id":invite.id,"delivery":delivery}

@app.post("/api/v1/payments/orders",status_code=201)
def payment_order(payload:PaymentOrderIn,user:User=Depends(require_permission("finance.payments.create_own")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    if not razorpay_enabled():raise HTTPException(status_code=503,detail={"code":"payment_unavailable","message":"Razorpay is not configured"})
    student=current_student_or_forbidden(db,user);invoice=db.get(Invoice,payload.invoice_id)
    if not invoice or invoice.student_id!=student.id:raise HTTPException(status_code=404,detail={"code":"not_found","message":"Invoice not found"})
    if invoice.status=="paid":raise HTTPException(status_code=409,detail={"code":"already_paid","message":"Invoice is already paid"})
    existing=db.query(Payment).filter_by(invoice_id=invoice.id,status="created").first()
    payment=existing or Payment(invoice_id=invoice.id,amount_paise=invoice.total_paise,idempotency_key=new_token())
    if not existing:db.add(payment);db.flush()
    try:
        gateway=create_order(invoice.number,payment.amount_paise,payment.idempotency_key)
    except Exception as exc:
        payment.status="failed";audit(db,user.id,"payment.order_failed","invoice",invoice.id);db.commit();raise HTTPException(status_code=503,detail={"code":"payment_unavailable","message":"Payment provider could not create an order"}) from exc
    payment.gateway_order_id=gateway["id"];payment.status="created";audit(db,user.id,"payment.order_created","payment",payment.id);db.commit();return {"payment_id":payment.id,"key_id":settings().razorpay_key_id,"order_id":payment.gateway_order_id,"amount":payment.amount_paise,"currency":"INR"}
@app.post("/api/v1/payments/verify")
def payment_verify(payload:PaymentVerifyIn,user:User=Depends(require_permission("finance.payments.verify_own")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    student=current_student_or_forbidden(db,user);payment=db.query(Payment).join(Invoice).filter(Payment.gateway_order_id==payload.razorpay_order_id,Invoice.student_id==student.id).first()
    if not payment:raise HTTPException(status_code=404,detail={"code":"not_found","message":"Payment order not found"})
    if not verify_payment_signature(payload.razorpay_order_id,payload.razorpay_payment_id,payload.razorpay_signature):raise HTTPException(status_code=400,detail={"code":"invalid_signature","message":"Payment signature is invalid"})
    payment.gateway_payment_id=payload.razorpay_payment_id;payment.status="verification_pending";audit(db,user.id,"payment.client_verified","payment",payment.id);db.commit();return {"status":"verification_pending","notice":"Payment is recorded only after a verified Razorpay webhook."}


@app.post("/api/v1/payments/webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    raw = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")

    if not verify_webhook(raw, signature):
        raise HTTPException(
            status_code=400,
            detail={"code": "invalid_signature", "message": "Webhook signature is invalid"},
        )

    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(
            status_code=400,
            detail={"code": "invalid_payload", "message": "Invalid webhook payload"},
        )

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Invalid webhook payload")

    event_type = payload.get("event")
    if not isinstance(event_type, str) or not event_type:
        raise HTTPException(status_code=400, detail="Webhook event type is missing")

    event_id = (
        request.headers.get("X-Razorpay-Event-Id")
        or hash_token(raw.decode("utf-8"))
    )
    if len(event_id) > 120:
        raise HTTPException(status_code=400, detail="Invalid event ID")

    event = PaymentGatewayEvent(
        gateway_event_id=event_id,
        signature_valid=True,
        event_type=event_type,
        payload=payload,
    )

    try:
        db.add(event)
        db.flush()

        if event_type == "payment.captured":
            payment_data = payload.get("payload")
            wrapper = payment_data.get("payment") if isinstance(payment_data, dict) else None
            entity = wrapper.get("entity") if isinstance(wrapper, dict) else None

            if not isinstance(entity, dict):
                raise HTTPException(status_code=400, detail="Invalid payment payload")

            order_id = entity.get("order_id")
            payment_id = entity.get("id")
            amount = entity.get("amount")
            currency = entity.get("currency")

            if (
                not isinstance(order_id, str) or not order_id
                or not isinstance(payment_id, str) or not payment_id
                or type(amount) is not int
                or currency != "INR"
                or entity.get("status") != "captured"
            ):
                raise HTTPException(
                    status_code=400,
                    detail={"code": "invalid_capture", "message": "Captured payment details are invalid"},
                )

            payment = (
                db.query(Payment)
                .filter_by(gateway_order_id=order_id)
                .with_for_update()
                .first()
            )

            if not payment:
                raise HTTPException(
                    status_code=409,
                    detail={"code": "order_not_found", "message": "Payment order is not recorded yet"},
                )

            invoice = payment.invoice

            if (
                payment.amount_paise != amount
                or invoice.total_paise != amount
                or payment.currency != currency
            ):
                raise HTTPException(
                    status_code=400,
                    detail={"code": "payment_mismatch", "message": "Payment details do not match the recorded invoice"},
                )

            if payment.gateway_payment_id and payment.gateway_payment_id != payment_id:
                raise HTTPException(
                    status_code=409,
                    detail={"code": "payment_already_completed", "message": "A different payment has already completed this order"},
                )

            if payment.status != "paid":
                payment.gateway_payment_id = payment_id
                payment.status = "paid"
                payment.paid_at = now()
                invoice.status = "paid"

                recipient = invoice.student.user.email
                delivery = deliver(
                    db,
                    recipient,
                    "payment_receipt",
                    invoice.student.user_id,
                )
                audit(
                    db,
                    None,
                    "payment.captured",
                    "payment",
                    payment.id,
                    {"delivery": delivery},
                )

        event.processed_at = now()
        db.commit()

    except IntegrityError:
        db.rollback()
        prior = db.query(PaymentGatewayEvent).filter_by(
            gateway_event_id=event_id
        ).first()
        if prior:
            return {"status": "duplicate"}

        raise HTTPException(
            status_code=409,
            detail={"code": "event_conflict", "message": "Webhook event could not be recorded"},
        )
    except Exception:
        db.rollback()
        raise

    return {"status": "accepted"}



@app.post("/api/v1/files/assignments/{assignment_id}",status_code=201)
async def upload_assignment_file(assignment_id:str,request:Request,user:User=Depends(require_permission("files.upload_own")),_csrf:User=Depends(require_csrf),db:Session=Depends(get_db)):
    student=current_student_or_forbidden(db,user);assignment=db.get(Assignment,assignment_id)
    if not assignment or assignment.offering.department_id!=student.department_id:raise HTTPException(status_code=404,detail={"code":"not_found","message":"Assignment not found"})
    content_type=request.headers.get("Content-Type","").split(";",1)[0];filename=request.headers.get("X-Filename","submission")[:255];data=await request.body();file=FileObject(storage_key="pending",original_name=filename,content_type=content_type,size=len(data),sha256="pending",uploaded_by=user.id,owner_student_id=student.id);db.add(file);db.flush()
    try:key,digest=save_private(data,content_type,filename,file.id)
    except ValueError as exc:db.delete(file);db.commit();raise HTTPException(status_code=422,detail={"code":"invalid_file","message":str(exc)})
    file.storage_key=key;file.sha256=digest
    try:file.scan_status=scan_file(data)
    except ScannerUnavailable:
        file.scan_status="unavailable";audit(db,user.id,"file.scan_unavailable","file",file.id)
    audit(db,user.id,"file.uploaded","file",file.id,{"scan_status":file.scan_status});db.commit();return {"id":file.id,"scan_status":file.scan_status,"notice":"Downloads remain disabled unless the configured malware scanner marks the file clean."}
@app.get("/api/v1/files/{file_id}")
def download_private_file(file_id:str,user:User=Depends(current_user),db:Session=Depends(get_db)):
    file=db.get(FileObject,file_id)
    if not file or file.scan_status!="clean":raise HTTPException(status_code=404,detail={"code":"not_found","message":"File is unavailable"})
    owner=db.get(Student,file.owner_student_id) if file.owner_student_id else None
    if not (owner and owner.user_id==user.id) and not roles(user).intersection({"college_admin","hod","principal"}):raise HTTPException(status_code=403,detail={"code":"forbidden","message":"File access denied"})
    path=private_path(file.storage_key)
    if not path.is_file():raise HTTPException(status_code=404,detail={"code":"not_found","message":"File is unavailable"})
    audit(db,user.id,"file.downloaded","file",file.id);db.commit();return FileResponse(path,media_type=file.content_type,filename=file.original_name)
