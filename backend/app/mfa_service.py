"""TOTP implementation; Fernet import is intentionally lazy so startup fails closed only when MFA is used."""
import base64,hmac,secrets,struct,time
from hashlib import sha1
from typing import Optional
from urllib.parse import quote
from .core import settings

def new_secret()->str:return base64.b32encode(secrets.token_bytes(20)).decode().rstrip("=")
def _totp(secret:str,timestamp:Optional[int]=None)->str:
    counter=int((timestamp or int(time.time()))//30);key=base64.b32decode(secret+"="*((8-len(secret)%8)%8));digest=hmac.new(key,struct.pack(">Q",counter),sha1).digest();offset=digest[-1]&15;number=(struct.unpack(">I",digest[offset:offset+4])[0]&0x7fffffff)%1_000_000;return f"{number:06d}"
def verify(secret:str,code:str)->bool:return any(hmac.compare_digest(_totp(secret,int(time.time())+delta),code) for delta in (-30,0,30))
def encrypt(secret:str)->str:
    if not settings().field_encryption_key:raise RuntimeError("MFA encryption key is not configured")
    from cryptography.fernet import Fernet
    return Fernet(settings().field_encryption_key.encode()).encrypt(secret.encode()).decode()
def decrypt(value:str)->str:
    from cryptography.fernet import Fernet
    return Fernet(settings().field_encryption_key.encode()).decrypt(value.encode()).decode()
def otpauth_uri(secret:str,email:str)->str:
    cfg=settings();label=quote(f"{cfg.mfa_issuer_name}:{email}");issuer=quote(cfg.mfa_issuer_name);return f"otpauth://totp/{label}?secret={secret}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
