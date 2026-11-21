
"""verification challenges and MFA recovery codes

Revision ID: 0004_verification_mfa_recovery
Revises: 0003_live_services
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text

revision = "0004_verification_mfa_recovery"
down_revision = "0003_live_services"
branch_labels = None
depends_on = None


def _inspector():
    return sa.inspect(op.get_bind())


def _columns(table):
    return {c["name"] for c in _inspector().get_columns(table)}


def _indexes(table):
    return {i["name"] for i in _inspector().get_indexes(table)}


def _ensure_columns(table, required):
    missing = required - _columns(table)
    if missing:
        raise RuntimeError(
            f"Existing table {table} is missing columns: {sorted(missing)}"
        )


def upgrade():
    if "mobile_number" not in _columns("users"):
        op.add_column("users", Column("mobile_number", String(20), nullable=True))

    if "mobile_verified_at" not in _columns("users"):
        op.add_column(
            "users",
            Column("mobile_verified_at", DateTime(timezone=True), nullable=True),
        )

    if "ix_users_mobile_number" not in _indexes("users"):
        op.create_index(
            "ix_users_mobile_number", "users", ["mobile_number"], unique=True
        )

    tables = set(_inspector().get_table_names())

    if "mfa_recovery_codes" not in tables:
        op.create_table(
            "mfa_recovery_codes",
            Column("id", String(36), primary_key=True),
            Column("user_id", String(36), ForeignKey("users.id"), nullable=False),
            Column("code_hash", String(64), nullable=False, unique=True),
            Column("used_at", DateTime(timezone=True), nullable=True),
            Column("created_at", DateTime(timezone=True),
                   server_default=text("now()"), nullable=False),
        )
    else:
        _ensure_columns(
            "mfa_recovery_codes",
            {"id", "user_id", "code_hash", "used_at", "created_at"},
        )

    if "ix_mfa_recovery_codes_user_id" not in _indexes("mfa_recovery_codes"):
        op.create_index(
            "ix_mfa_recovery_codes_user_id", "mfa_recovery_codes", ["user_id"]
        )

    if "verification_challenges" not in tables:
        op.create_table(
            "verification_challenges",
            Column("id", String(36), primary_key=True),
            Column("user_id", String(36), ForeignKey("users.id"), nullable=False),
            Column("destination", String(255), nullable=False),
            Column("channel", String(12), nullable=False),
            Column("purpose", String(40), nullable=False),
            Column("otp_hash", String(64), nullable=False),
            Column("requested_ip", String(64), nullable=False),
            Column("expires_at", DateTime(timezone=True), nullable=False),
            Column("attempts", Integer, nullable=False, server_default="0"),
            Column("consumed_at", DateTime(timezone=True), nullable=True),
            Column("created_at", DateTime(timezone=True),
                   server_default=text("now()"), nullable=False),
        )
    else:
        _ensure_columns(
            "verification_challenges",
            {
                "id", "user_id", "destination", "channel", "purpose",
                "otp_hash", "requested_ip", "expires_at", "attempts",
                "consumed_at", "created_at",
            },
        )

    if "ix_verification_challenges_user_id" not in _indexes(
        "verification_challenges"
    ):
        op.create_index(
            "ix_verification_challenges_user_id",
            "verification_challenges",
            ["user_id"],
        )

    if "ix_verification_challenges_destination" not in _indexes(
        "verification_challenges"
    ):
        op.create_index(
            "ix_verification_challenges_destination",
            "verification_challenges",
            ["destination"],
        )


def downgrade():
    raise RuntimeError(
        "This migration is intentionally irreversible to protect existing data."
    )
