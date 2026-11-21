from datetime import date,datetime
from typing import Optional
from pydantic import BaseModel,EmailStr,Field
class LoginIn(BaseModel):email:EmailStr;password:str=Field(min_length=8,max_length=256);mfa_code:Optional[str]=Field(default=None,pattern="^\\d{6}$");mfa_recovery_code:Optional[str]=Field(default=None,min_length=8,max_length=128)
class EnquiryIn(BaseModel):name:str=Field(min_length=2,max_length=100);contact:str=Field(min_length=3,max_length=150);message:str=Field(min_length=2,max_length=2000);website:str=""
class AttendanceItem(BaseModel):student_id:str;status:str=Field(pattern="^(present|absent|od|leave)$")
class AttendanceIn(BaseModel):offering_id:str;session_date:date;records:list[AttendanceItem]=Field(min_length=1)
class AssignmentIn(BaseModel):offering_id:str;title:str=Field(min_length=2,max_length=200);instructions:str=Field(min_length=2,max_length=5000);due_at:datetime;max_marks:int=Field(gt=0,le=1000)
class ResultIn(BaseModel):student_id:str;subject_code:str;exam_name:str;marks:int=Field(ge=0,le=100);grade:str=Field(min_length=1,max_length=8)
class CircularIn(BaseModel):title:str=Field(min_length=2,max_length=200);body:str=Field(min_length=2,max_length=10000);audience:dict={}
class SubmissionIn(BaseModel):note:str=Field(min_length=2,max_length=5000)
class LeaveRequestIn(BaseModel):from_date:date;to_date:date;reason:str=Field(min_length=3,max_length=2000)
class ProfileIn(BaseModel):full_name:str=Field(min_length=2,max_length=200)
class AdminStudentIn(BaseModel):email:EmailStr;full_name:str=Field(min_length=2,max_length=200);register_number:str=Field(min_length=3,max_length=60);department_id:str;programme:str=Field(min_length=2,max_length=200);password:str=Field(min_length=12,max_length=256)
class PasswordResetRequestIn(BaseModel):email:EmailStr
class PasswordResetConfirmIn(BaseModel):token:str=Field(min_length=20,max_length=256);new_password:str=Field(min_length=12,max_length=256)
class PasswordChangeIn(BaseModel):current_password:str=Field(min_length=8,max_length=256);new_password:str=Field(min_length=12,max_length=256)
class MfaVerifyIn(BaseModel):code:str=Field(pattern="^\\d{6}$")
class OtpVerifyIn(BaseModel):code:str=Field(pattern="^\\d{6}$")
class MobileVerificationRequestIn(BaseModel):mobile_number:str=Field(min_length=10,max_length=20)
class PaymentOrderIn(BaseModel):invoice_id:str
class PaymentVerifyIn(BaseModel):razorpay_order_id:str=Field(min_length=5,max_length=120);razorpay_payment_id:str=Field(min_length=5,max_length=120);razorpay_signature:str=Field(min_length=64,max_length=64,pattern="^[0-9a-fA-F]{64}$")
class InvitationAcceptIn(BaseModel):token:str=Field(min_length=20,max_length=256);password:str=Field(min_length=12,max_length=256)
class ScanStatusIn(BaseModel):scan_status:str=Field(pattern="^(clean|rejected)$")
