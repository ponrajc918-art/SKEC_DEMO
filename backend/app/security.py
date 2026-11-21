
from __future__ import annotations

from datetime import timedelta
import secrets
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session, joinedload

from .core import get_db, hash_token, new_token, now, settings, verify_password
from .models import AuditLog, MfaFactor, PasswordHistory, Permission, Role, RolePermission, SessionRecord, User, UserRole


def audit(
    db: Session,
    actor: Optional[str],
    action: str,
    target_type: str,
    target_id: Optional[str],
    summary: Optional[dict] = None,
):
    db.add(
        AuditLog(
            actor_user_id=actor,
            action=action,
            target_type=target_type,
            target_id=target_id,
            summary=summary or {},
        )
    )


def roles(user: User) -> set[str]:
    return {r.role.code for r in user.roles}


def permissions(user: User) -> set[str]:
    return {
        permission.code
        for membership in user.roles
        for assignment in membership.role.permissions
        for permission in [assignment.permission]
    }


def password_was_used(db: Session, user: User, candidate: str) -> bool:
    if verify_password(candidate, user.password_hash):
        return True
    rows = (
        db.query(PasswordHistory)
        .filter_by(user_id=user.id)
        .order_by(PasswordHistory.created_at.desc())
        .limit(settings().password_history_count)
        .all()
    )
    return any(verify_password(candidate, row.password_hash) for row in rows)


def remember_replaced_password(db: Session, user: User) -> None:
    db.add(PasswordHistory(user_id=user.id, password_hash=user.password_hash))


def current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    raw = request.cookies.get(settings().session_cookie_name)

    if not raw:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "unauthenticated",
                "message": "Sign in required",
            },
        )

    record = (
        db.query(SessionRecord)
        .options(
            joinedload(SessionRecord.user)
            .joinedload(User.roles)
            .joinedload(UserRole.role)
            .joinedload(Role.permissions)
            .joinedload(RolePermission.permission)
        )
        .filter(
            SessionRecord.id == hash_token(raw),
            SessionRecord.revoked_at.is_(None),
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "session_expired",
                "message": "Session expired",
            },
        )

    current_time = now()

    expires_at = record.expires_at
    last_seen_at = record.last_seen_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=current_time.tzinfo)

    if last_seen_at.tzinfo is None:
        last_seen_at = last_seen_at.replace(tzinfo=current_time.tzinfo)

    idle_limit = timedelta(
        minutes=settings().session_idle_timeout_minutes
    )

    absolute_expired = expires_at <= current_time
    idle_expired = last_seen_at <= current_time - idle_limit

    if absolute_expired or idle_expired:
        record.revoked_at = current_time
        db.commit()

        raise HTTPException(
            status_code=401,
            detail={
                "code": "session_expired",
                "message": "Session expired. Please sign in again.",
            },
        )

    record.last_seen_at = current_time
    db.commit()

    user = record.user

    # Enforce mandatory MFA for privileged accounts in production.
    if settings().app_env == "production":
        required_roles = {
            role.strip()
            for role in settings().mfa_required_roles.split(",")
            if role.strip()
        }

        if roles(user).intersection(required_roles):
            factor = (
                db.query(MfaFactor)
                .filter(MfaFactor.user_id == user.id)
                .first()
            )

            mfa_confirmed = bool(
                factor and factor.confirmed_at
            )

            allowed_paths = {
                "/api/v1/auth/mfa/enroll",
                "/api/v1/auth/mfa/confirm",
                "/api/v1/auth/me",
                "/api/v1/auth/logout",
                "/api/v1/auth/sign-out-everywhere",
                "/api/v1/auth/password/change",
                "/api/v1/auth/mfa/recovery-codes",
                "/api/v1/auth/email-verification/request",
                "/api/v1/auth/email-verification/confirm",
                "/api/v1/auth/mobile-verification/request",
                "/api/v1/auth/mobile-verification/confirm",
            }

            if not mfa_confirmed and request.url.path not in allowed_paths:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "code": "mfa_enrollment_required",
                        "message": (
                            "Complete mandatory authenticator "
                            "enrollment before accessing this resource."
                        ),
                    },
                )

    return user


def require_csrf(
    request: Request,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> User:
    submitted = request.headers.get("X-CSRF-Token")
    raw = request.cookies.get(settings().session_cookie_name)

    record = db.get(SessionRecord, hash_token(raw or ""))

    if (
        not submitted
        or not record
        or not secrets.compare_digest(
            record.csrf_hash,
            hash_token(submitted),
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "csrf_failed",
                "message": "Request verification failed",
            },
        )

    return user


def require(*allowed: str):
    def checker(
        user: User = Depends(current_user),
    ) -> User:
        if not roles(user).intersection(allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "forbidden",
                    "message": "Permission denied",
                },
            )

        return user

    return checker


def require_permission(*allowed: str):
    def checker(user: User = Depends(current_user)) -> User:
        if not permissions(user).intersection(allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "forbidden", "message": "Permission denied"},
            )
        return user
    return checker


def create_session(
    db: Session,
    user: User,
) -> tuple[str, str]:
    token, csrf = new_token(), new_token()

    record = SessionRecord(
        id=hash_token(token),
        user_id=user.id,
        csrf_hash=hash_token(csrf),
        expires_at=now() + timedelta(
            hours=settings().session_absolute_timeout_hours
        ),
    )

    db.add(record)

    audit(
        db,
        user.id,
        "auth.login",
        "user",
        user.id,
    )

    db.commit()

    return token, csrf
