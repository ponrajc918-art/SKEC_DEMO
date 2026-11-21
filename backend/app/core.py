from __future__ import annotations
import hashlib, hmac, os, secrets
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Generator
from argon2 import PasswordHasher
from fastapi import Cookie, Depends, HTTPException, Request, status
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env", extra="ignore")
    database_url:str=os.getenv("DATABASE_URL","sqlite:///./skec.db")
    session_secret:str=os.getenv("SESSION_SECRET","development-only-change-me")
    app_env:str=os.getenv("APP_ENV","development")
    session_cookie_name:str="skec_session"
    session_idle_timeout_minutes:int=30
    session_absolute_timeout_hours:int=12
    password_history_count:int=int(os.getenv("PASSWORD_HISTORY_COUNT","5"))
    backend_cors_origins:str=os.getenv("BACKEND_CORS_ORIGINS","http://localhost:3000")
    public_site_url:str=os.getenv("PUBLIC_SITE_URL","http://localhost:3000")
    email_mode:str=os.getenv("EMAIL_MODE","mock")
    smtp_host:str=os.getenv("SMTP_HOST","")
    smtp_port:int=int(os.getenv("SMTP_PORT","587"))
    smtp_username:str=os.getenv("SMTP_USERNAME","")
    smtp_password:str=os.getenv("SMTP_PASSWORD","")
    email_from_address:str=os.getenv("EMAIL_FROM_ADDRESS","")
    smtp_use_tls:bool=os.getenv("SMTP_USE_TLS","true").lower()=="true"
    sms_provider:str=os.getenv("SMS_PROVIDER","disabled")
    sms_endpoint:str=os.getenv("SMS_ENDPOINT","")
    sms_api_token:str=os.getenv("SMS_API_TOKEN","")
    sms_sender_id:str=os.getenv("SMS_SENDER_ID","")
    default_country_code:str=os.getenv("DEFAULT_COUNTRY_CODE","+91")
    otp_expiry_minutes:int=int(os.getenv("OTP_EXPIRY_MINUTES","10"))
    otp_max_attempts:int=int(os.getenv("OTP_MAX_ATTEMPTS","5"))
    otp_resend_cooldown_seconds:int=int(os.getenv("OTP_RESEND_COOLDOWN_SECONDS","60"))
    razorpay_key_id:str=os.getenv("RAZORPAY_KEY_ID","")
    razorpay_key_secret:str=os.getenv("RAZORPAY_KEY_SECRET","")
    razorpay_webhook_secret:str=os.getenv("RAZORPAY_WEBHOOK_SECRET","")
    payment_mode:str=os.getenv("PAYMENT_MODE","test")
    allow_live_payments:bool=os.getenv("ALLOW_LIVE_PAYMENTS","false").lower()=="true"
    private_storage_root:str=os.getenv("PRIVATE_STORAGE_ROOT","./private-storage")
    private_upload_max_bytes:int=int(os.getenv("PRIVATE_UPLOAD_MAX_BYTES",str(10*1024*1024)))
    file_scanner_mode:str=os.getenv("FILE_SCANNER_MODE","disabled")
    clamd_host:str=os.getenv("CLAMD_HOST","")
    clamd_port:int=int(os.getenv("CLAMD_PORT","3310"))
    clamd_timeout_seconds:int=int(os.getenv("CLAMD_TIMEOUT_SECONDS","15"))
    field_encryption_key:str=os.getenv("FIELD_ENCRYPTION_KEY","")
    mfa_issuer_name:str=os.getenv("MFA_ISSUER_NAME","SKEC Digital Campus")
    mfa_required_roles:str=os.getenv("MFA_REQUIRED_ROLES","principal,hod,college_admin")
@lru_cache
def settings()->Settings:return Settings()
def allowed_origins()->list[str]:return [origin.strip() for origin in settings().backend_cors_origins.split(",") if origin.strip()]
def validate_production_settings()->None:
    cfg=settings()
    if cfg.app_env != "production": return
    if cfg.session_secret == "development-only-change-me" or len(cfg.session_secret) < 48: raise RuntimeError("Production SESSION_SECRET must contain at least 48 random characters")
    if cfg.database_url.startswith("sqlite"): raise RuntimeError("Production requires PostgreSQL, not SQLite")
    if not allowed_origins() or "*" in allowed_origins(): raise RuntimeError("Production BACKEND_CORS_ORIGINS must list explicit HTTPS origins")
    if any(not origin.startswith("https://") for origin in allowed_origins()): raise RuntimeError("Production BACKEND_CORS_ORIGINS must use HTTPS origins")
    if cfg.email_mode not in {"smtp","disabled"}: raise RuntimeError("Production EMAIL_MODE must be smtp or disabled")
    if cfg.email_mode=="smtp" and not all([cfg.smtp_host,cfg.smtp_username,cfg.smtp_password,cfg.email_from_address]): raise RuntimeError("Production SMTP configuration is incomplete")
    if cfg.sms_provider not in {"disabled","generic_http"}: raise RuntimeError("Production SMS_PROVIDER is unsupported")
    if cfg.sms_provider=="generic_http" and not all([cfg.sms_endpoint,cfg.sms_api_token,cfg.sms_sender_id]): raise RuntimeError("Production SMS configuration is incomplete")
    if cfg.file_scanner_mode not in {"disabled","clamd"}: raise RuntimeError("Production FILE_SCANNER_MODE is unsupported")
    if cfg.file_scanner_mode=="clamd" and not cfg.clamd_host: raise RuntimeError("Production CLAMD_HOST is required when FILE_SCANNER_MODE=clamd")
    if cfg.payment_mode == "live" and not cfg.allow_live_payments: raise RuntimeError("Live payments require ALLOW_LIVE_PAYMENTS=true")
    if not cfg.field_encryption_key: raise RuntimeError("Production FIELD_ENCRYPTION_KEY is required for MFA secret protection")
engine=create_engine(settings().database_url, future=True, connect_args={"check_same_thread":False} if settings().database_url.startswith("sqlite") else {})
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
passwords=PasswordHasher()
def now()->datetime:return datetime.now(timezone.utc)
def is_expired(value:datetime)->bool:return value.replace(tzinfo=timezone.utc) < now() if value.tzinfo is None else value < now()
def get_db()->Generator[Session,None,None]:
    db=SessionLocal()
    try:yield db
    finally:db.close()
def hash_token(value:str)->str:return hashlib.sha256(value.encode()).hexdigest()
def hash_otp(value:str)->str:
    """Keyed OTP storage prevents inexpensive offline recovery of six-digit codes."""
    return hmac.new(settings().session_secret.encode(),value.encode(),hashlib.sha256).hexdigest()
def hash_password(value:str)->str:return passwords.hash(value)
def verify_password(value:str, hashed:str)->bool:
    try:return passwords.verify(hashed,value)
    except Exception:return False
def password_policy_error(value:str)->str|None:
    if len(value)<12:return "Password must contain at least 12 characters"
    if len(value)>256:return "Password is too long"
    if not any(char.islower() for char in value):return "Password must include a lowercase letter"
    if not any(char.isupper() for char in value):return "Password must include an uppercase letter"
    if not any(char.isdigit() for char in value):return "Password must include a number"
    if not any(not char.isalnum() for char in value):return "Password must include a symbol"
    return None
def new_token()->str:return secrets.token_urlsafe(32)
def deny(detail:str="Not authorised")->HTTPException:return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"code":"forbidden","message":detail})
