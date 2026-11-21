import os
import json
import hmac
from pathlib import Path
os.environ["DATABASE_URL"]="sqlite:///./test_skec.db"
Path("test_skec.db").unlink(missing_ok=True)
from fastapi.testclient import TestClient
from app.main import app
from app.core import SessionLocal,hash_otp,hash_token,new_token,now
from datetime import timedelta
from app.models import EmailDelivery,Invitation,PasswordResetToken,Permission,Role,User,Invoice,Payment,PaymentGatewayEvent,Student,VerificationChallenge
from app.core import hash_password
from app.payment_service import verify_payment_signature,verify_webhook
from app.mfa_service import _totp,new_secret,verify as verify_totp
def csrf(client):return {"X-CSRF-Token":client.cookies.get("skec_csrf","")}
def test_health_and_demo_login():
    with TestClient(app) as client:
        assert client.get("/api/v1/health").json()["status"]=="ok"
        response=client.post("/api/v1/auth/login",json={"email":"student.demo@skec.example","password":"DemoPass!2026"})
        assert response.status_code==200
        assert client.get("/api/v1/auth/me").json()["roles"]==["student"]
        assert client.get("/api/v1/results/mine").json()["results"][0]["grade"]=="A"
def test_enquiry_is_persisted():
    with TestClient(app) as client:
        response=client.post("/api/v1/enquiries",json={"name":"Test Enquirer","contact":"test@example.com","message":"Please share information."})
        assert response.status_code==201 and response.json()["status"]=="saved"

def test_student_demo_workflow_and_authorisation():
    with TestClient(app) as client:
        assert client.post("/api/v1/auth/login",json={"email":"student.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        assert len(client.get("/api/v1/dashboard").json()["metrics"])==3
        assignments=client.get("/api/v1/assignments/mine").json()["assignments"]
        assert client.post(f"/api/v1/assignments/{assignments[0]['id']}/submissions",json={"note":"Unverified request."}).status_code==403
        assert assignments and client.post(f"/api/v1/assignments/{assignments[0]['id']}/submissions",json={"note":"Synthetic demo submission."},headers=csrf(client)).status_code==201
        assert client.get("/api/v1/timetable/mine").status_code==200
        assert client.get("/api/v1/admin/users").status_code==403

def test_faculty_and_admin_demo_workflows():
    with TestClient(app) as faculty:
        assert faculty.post("/api/v1/auth/login",json={"email":"faculty.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        teaching=faculty.get("/api/v1/teaching/mine").json()
        assert teaching["subjects"] and teaching["students"]
    with TestClient(app) as admin:
        assert admin.post("/api/v1/auth/login",json={"email":"admin.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        assert len(admin.get("/api/v1/admin/users").json()["users"])>=8

def test_private_file_access_requires_clean_scan_and_owner_scope(monkeypatch,tmp_path):
    from app.core import settings
    monkeypatch.setenv("PRIVATE_STORAGE_ROOT",str(tmp_path));settings.cache_clear()
    monkeypatch.setattr("app.main.scan_file",lambda _data:"clean")
    with TestClient(app) as student:
        assert student.post("/api/v1/auth/login",json={"email":"student.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        assignment=student.get("/api/v1/assignments/mine").json()["assignments"][0]
        upload=student.post(f"/api/v1/files/assignments/{assignment['id']}",content=b"demo submission",headers={**csrf(student),"Content-Type":"text/plain","X-Filename":"demo.txt"})
        assert upload.status_code==201;file_id=upload.json()["id"]
        assert upload.json()["scan_status"]=="clean"
        assert student.get(f"/api/v1/files/{file_id}").content==b"demo submission"
        with TestClient(app) as other_student:
            assert other_student.post("/api/v1/auth/login",json={"email":"student2.demo@skec.example","password":"DemoPass!2026"}).status_code==200
            assert other_student.get(f"/api/v1/files/{file_id}").status_code==403
    settings.cache_clear()

def test_email_otp_is_hashed_single_use_and_rate_limited(monkeypatch):
    monkeypatch.setattr("app.main.new_otp",lambda:"123456")
    with TestClient(app) as client:
        assert client.post("/api/v1/auth/login",json={"email":"student.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        issued=client.post("/api/v1/auth/email-verification/request",headers=csrf(client))
        assert issued.status_code==200 and "123456" not in issued.text
        assert client.post("/api/v1/auth/email-verification/confirm",json={"code":"000000"},headers=csrf(client)).status_code==400
        assert client.post("/api/v1/auth/email-verification/confirm",json={"code":"123456"},headers=csrf(client)).status_code==200
        assert client.post("/api/v1/auth/email-verification/confirm",json={"code":"123456"},headers=csrf(client)).status_code==400
    db=SessionLocal()
    try:
        challenge=db.query(VerificationChallenge).filter_by(channel="email",purpose="email_verification").order_by(VerificationChallenge.created_at.desc()).first()
        assert challenge and challenge.otp_hash==hash_otp("123456") and challenge.otp_hash!=hash_token("123456") and challenge.consumed_at is not None
    finally: db.close()

def test_mobile_otp_reports_unavailable_without_creating_a_mobile_identity():
    with TestClient(app) as client:
        assert client.post("/api/v1/auth/login",json={"email":"student2.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        response=client.post("/api/v1/auth/mobile-verification/request",json={"mobile_number":"+919876543210"},headers=csrf(client))
        assert response.status_code==503
        assert client.get("/api/v1/auth/me").json()["mobile_number"] is None

def test_central_permission_catalogue_protects_admin_resources():
    db=SessionLocal()
    try:
        assert {"super_admin","exam_staff","accounts_staff"}.issubset({row.code for row in db.query(Role).all()})
        assert db.query(Permission).filter_by(code="admin.users.read").one()
    finally: db.close()
    with TestClient(app) as student:
        assert student.post("/api/v1/auth/login",json={"email":"student.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        assert student.get("/api/v1/admin/users").status_code==403
    with TestClient(app) as admin:
        assert admin.post("/api/v1/auth/login",json={"email":"admin.demo@skec.example","password":"DemoPass!2026"}).status_code==200
        assert admin.get("/api/v1/admin/users").status_code==200

def test_login_rate_limit_applies_to_account_identifier():
    with TestClient(app) as client:
        for _ in range(5):
            assert client.post("/api/v1/auth/login",json={"email":"lockout.target@example.com","password":"WrongPassword!2026"}).status_code==401
        assert client.post("/api/v1/auth/login",json={"email":"lockout.target@example.com","password":"WrongPassword!2026"}).status_code==429

def test_password_reset_mock_delivery_and_token_lifecycle():
    with TestClient(app) as client:
        assert client.post("/api/v1/auth/password-reset/request",json={"email":"student.demo@skec.example"}).status_code==200
        db=SessionLocal();user=db.query(User).filter_by(email="student.demo@skec.example").one()
        assert db.query(EmailDelivery).filter_by(user_id=user.id,template="password_reset",status="mocked").count()==1
        raw=new_token();db.add(PasswordResetToken(user_id=user.id,token_hash=hash_token(raw),purpose="password_reset",expires_at=now().replace(year=now().year+1)));db.commit();db.close()
        assert client.post("/api/v1/auth/password-reset/confirm",json={"token":raw,"new_password":"ChangedDemoPass!2026"}).status_code==200
        assert client.post("/api/v1/auth/login",json={"email":"student.demo@skec.example","password":"ChangedDemoPass!2026"}).status_code==200

def test_razorpay_signature_and_webhook_helpers(monkeypatch):
    monkeypatch.setenv("RAZORPAY_KEY_SECRET","test_secret")
    from app.core import settings
    settings.cache_clear()
    signature=hmac.new(b"test_secret",b"order_1|pay_1",__import__("hashlib").sha256).hexdigest()
    assert verify_payment_signature("order_1","pay_1",signature)
    webhook=hmac.new(b"webhook_secret",b'{"event":"payment.captured"}',__import__("hashlib").sha256).hexdigest()
    monkeypatch.setenv("RAZORPAY_WEBHOOK_SECRET","webhook_secret");settings.cache_clear()
    assert verify_webhook(b'{"event":"payment.captured"}',webhook)
    settings.cache_clear()

def test_totp_algorithm_accepts_only_current_code():
    secret=new_secret();code=_totp(secret)
    assert verify_totp(secret,code)
    assert not verify_totp(secret,"000000")
def test_invitation_acceptance_verifies_email_and_prevents_reuse():
    raw=new_token()

    db=SessionLocal()
    user=User(
        email="invitation.test@example.com",
        password_hash=hash_password("TemporaryPass!2026"),
        status="invited",
        must_change_password=True
    )
    inviter=db.query(User).filter_by(email="admin.demo@skec.example").one()
    db.add(user)
    db.flush()

    invitation=Invitation(
        user_id=user.id,
        token_hash=hash_token(raw),
        expires_at=now()+timedelta(days=1),
        invited_by=inviter.id
    )
    db.add(invitation)
    db.commit()
    user_id=user.id
    db.close()

    with TestClient(app) as client:
        response=client.post(
            "/api/v1/auth/invitations/accept",
            json={
                "token":raw,
                "password":"NewSecurePass!2026"
            }
        )
        assert response.status_code==200
        assert response.json()["message"]=="account_activated"

        reused=client.post(
            "/api/v1/auth/invitations/accept",
            json={
                "token":raw,
                "password":"AnotherSecurePass!2026"
            }
        )
        assert reused.status_code==400

    db=SessionLocal()
    accepted_user=db.get(User,user_id)
    accepted_invitation=db.query(Invitation).filter_by(
        user_id=user_id
    ).one()

    assert accepted_user.status=="active"
    assert accepted_user.must_change_password is False
    assert accepted_user.email_verified_at is not None
    assert accepted_invitation.accepted_at is not None

    assert __import__("app.core",fromlist=["verify_password"]).verify_password(
        "NewSecurePass!2026",
        accepted_user.password_hash
    )

    db.delete(accepted_invitation)
    db.delete(accepted_user)
    db.commit()
    db.close()
def _create_webhook_test_payment():
    db = SessionLocal()
    try:
        student = db.query(Student).filter_by(
            register_number="DEMO-CSE-001"
        ).one()

        invoice = Invoice(
            student_id=student.id,
            number=f"TEST-{new_token()[:12]}",
            total_paise=100000,
            status="open",
        )
        db.add(invoice)
        db.flush()

        payment = Payment(
            invoice_id=invoice.id,
            amount_paise=100000,
            currency="INR",
            status="created",
            gateway="razorpay",
            gateway_order_id=f"order_{new_token()[:20]}",
            idempotency_key=new_token(),
        )
        db.add(payment)
        db.commit()

        return payment.id, payment.gateway_order_id, invoice.id
    finally:
        db.close()


def _signed_webhook(payload, event_id="evt_test_001"):
    raw = json.dumps(payload).encode()
    signature = hmac.new(
        b"webhook_test_secret",
        raw,
        __import__("hashlib").sha256,
    ).hexdigest()

    return raw, {
        "X-Razorpay-Signature": signature,
        "X-Razorpay-Event-Id": event_id,
        "Content-Type": "application/json",
    }
def test_webhook_rejects_invalid_signature_without_storing_event(monkeypatch):
    from app.core import settings

    monkeypatch.setenv("RAZORPAY_WEBHOOK_SECRET", "webhook_test_secret")
    settings.cache_clear()

    try:
        with TestClient(app) as client:
            raw = json.dumps({"event": "payment.captured"}).encode()

            response = client.post(
                "/api/v1/payments/webhook",
                content=raw,
                headers={
                    "X-Razorpay-Signature": "0" * 64,
                    "X-Razorpay-Event-Id": "evt_invalid_signature",
                },
            )

            assert response.status_code == 400

            db = SessionLocal()
            try:
                assert db.query(PaymentGatewayEvent).filter_by(
                    gateway_event_id="evt_invalid_signature"
                ).count() == 0
            finally:
                db.close()
    finally:
        settings.cache_clear()


def test_webhook_captures_payment_and_rejects_duplicate_event(monkeypatch):
    from app.core import settings

    monkeypatch.setenv("RAZORPAY_WEBHOOK_SECRET", "webhook_test_secret")
    settings.cache_clear()

    try:
        with TestClient(app) as client:
            payment_id, order_id, invoice_id = _create_webhook_test_payment()

            payload = {
                "event": "payment.captured",
                "payload": {
                    "payment": {
                        "entity": {
                            "id": "pay_test_capture_001",
                            "order_id": order_id,
                            "amount": 100000,
                            "currency": "INR",
                            "status": "captured",
                        }
                    }
                },
            }

            raw, headers = _signed_webhook(
                payload,
                "evt_valid_capture_001",
            )

            response = client.post(
                "/api/v1/payments/webhook",
                content=raw,
                headers=headers,
            )

            assert response.status_code == 200
            assert response.json()["status"] == "accepted"

            db = SessionLocal()
            try:
                payment = db.get(Payment, payment_id)
                invoice = db.get(Invoice, invoice_id)
                event = db.query(PaymentGatewayEvent).filter_by(
                    gateway_event_id="evt_valid_capture_001"
                ).one()

                assert payment.status == "paid"
                assert payment.gateway_payment_id == "pay_test_capture_001"
                assert payment.paid_at is not None
                assert invoice.status == "paid"
                assert event.processed_at is not None
            finally:
                db.close()

            duplicate = client.post(
                "/api/v1/payments/webhook",
                content=raw,
                headers=headers,
            )

            assert duplicate.status_code == 200
            assert duplicate.json()["status"] == "duplicate"
    finally:
        settings.cache_clear()


def test_webhook_rejects_amount_mismatch_without_completing_payment(monkeypatch):
    from app.core import settings

    monkeypatch.setenv("RAZORPAY_WEBHOOK_SECRET", "webhook_test_secret")
    settings.cache_clear()

    try:
        with TestClient(app) as client:
            payment_id, order_id, invoice_id = _create_webhook_test_payment()

            payload = {
                "event": "payment.captured",
                "payload": {
                    "payment": {
                        "entity": {
                            "id": "pay_test_mismatch_001",
                            "order_id": order_id,
                            "amount": 99999,
                            "currency": "INR",
                            "status": "captured",
                        }
                    }
                },
            }

            raw, headers = _signed_webhook(
                payload,
                "evt_amount_mismatch_001",
            )

            response = client.post(
                "/api/v1/payments/webhook",
                content=raw,
                headers=headers,
            )

            assert response.status_code == 400

            db = SessionLocal()
            try:
                payment = db.get(Payment, payment_id)
                invoice = db.get(Invoice, invoice_id)

                assert payment.status == "created"
                assert payment.gateway_payment_id is None
                assert invoice.status == "open"
                assert db.query(PaymentGatewayEvent).filter_by(
                    gateway_event_id="evt_amount_mismatch_001"
                ).count() == 0
            finally:
                db.close()
    finally:
        settings.cache_clear()

def test_mobile_number_is_saved_only_after_successful_otp(monkeypatch):
    monkeypatch.setattr("app.main.new_otp", lambda: "123456")
    monkeypatch.setattr("app.main.send_otp", lambda destination, code: None)

    with TestClient(app) as client:
        assert client.post(
            "/api/v1/auth/login",
            json={"email": "student2.demo@skec.example", "password": "DemoPass!2026"},
        ).status_code == 200

        mobile = "+919876543210"
        requested = client.post(
            "/api/v1/auth/mobile-verification/request",
            json={"mobile_number": mobile},
            headers=csrf(client),
        )
        assert requested.status_code == 200

        profile = client.get("/api/v1/auth/me").json()
        assert profile["mobile_number"] is None
        assert profile["mobile_verified"] is False

        wrong = client.post(
            "/api/v1/auth/mobile-verification/confirm",
            json={"code": "000000"},
            headers=csrf(client),
        )
        assert wrong.status_code == 400
        assert client.get("/api/v1/auth/me").json()["mobile_number"] is None

        confirmed = client.post(
            "/api/v1/auth/mobile-verification/confirm",
            json={"code": "123456"},
            headers=csrf(client),
        )
        assert confirmed.status_code == 200

        profile = client.get("/api/v1/auth/me").json()
        assert profile["mobile_number"] == mobile
        assert profile["mobile_verified"] is True


def test_email_otp_cannot_verify_a_different_destination(monkeypatch):
    monkeypatch.setattr("app.main.new_otp", lambda: "123456")

    with TestClient(app) as client:
        assert client.post(
            "/api/v1/auth/login",
            json={"email": "student2.demo@skec.example", "password": "DemoPass!2026"},
        ).status_code == 200

        requested = client.post(
            "/api/v1/auth/email-verification/request",
            headers=csrf(client),
        )
        assert requested.status_code == 200

        db = SessionLocal()
        try:
            challenge = (
                db.query(VerificationChallenge)
                .filter_by(
                    channel="email",
                    purpose="email_verification",
                    consumed_at=None,
                )
                .order_by(VerificationChallenge.created_at.desc())
                .first()
            )
            assert challenge is not None
            challenge.destination = "different@example.com"
            db.commit()
        finally:
            db.close()

        response = client.post(
            "/api/v1/auth/email-verification/confirm",
            json={"code": "123456"},
            headers=csrf(client),
        )
        assert response.status_code == 400