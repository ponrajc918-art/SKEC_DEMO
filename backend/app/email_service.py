from __future__ import annotations
"""SMTP is opt-in. Development defaults to a recorded mock delivery."""
from email.message import EmailMessage
import smtplib
from sqlalchemy.orm import Session
from .core import settings
from .models import EmailDelivery

TEMPLATES={
    "password_reset":("Reset your SKEC Digital Campus password","Use this secure reset link: {link}"),
    "invitation":("Your SKEC Digital Campus invitation","Set your password using this secure link: {link}"),
    "password_changed":("Your SKEC password was changed","If you did not make this change, contact the college administrator immediately."),
    "payment_receipt":("SKEC payment receipt","Your verified payment has been recorded."),
    "email_otp":("Your SKEC verification code","Your verification code is {code}. It expires in {expires_minutes} minutes."),
    "circular":("New SKEC circular","A new circular is available in the campus portal."),
    "assignment":("SKEC assignment update","An assignment requires your attention in the campus portal."),
}
def deliver(db:Session,recipient:str,template:str,user_id:str|None=None,**values)->str:
    subject,body=TEMPLATES[template];body=body.format(**values)
    cfg=settings();status="disabled" if cfg.email_mode=="disabled" else "mocked";error=None
    if cfg.email_mode=="smtp":
        try:
            if not all([cfg.smtp_host,cfg.smtp_username,cfg.smtp_password,cfg.email_from_address]):raise RuntimeError("SMTP configuration is incomplete")
            msg=EmailMessage();msg["Subject"]=subject;msg["From"]=cfg.email_from_address;msg["To"]=recipient;msg.set_content(body)
            with smtplib.SMTP(cfg.smtp_host,cfg.smtp_port,timeout=15) as server:
                if cfg.smtp_use_tls: server.starttls()
                server.login(cfg.smtp_username,cfg.smtp_password);server.send_message(msg)
            status="sent"
        except Exception as exc:
            status="failed";error="delivery_failed"
    db.add(EmailDelivery(user_id=user_id,recipient=recipient,template=template,status=status,error=error));return status
