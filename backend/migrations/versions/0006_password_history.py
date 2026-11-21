
"""password history

Revision ID: 0006_password_history
Revises: 0005_permission_catalogue
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column, DateTime, ForeignKey, String, text

revision = "0006_password_history"
down_revision = "0005_permission_catalogue"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())

    if "password_history" not in tables:
        op.create_table(
            "password_history",
            Column("id", String(36), primary_key=True),
            Column("user_id", String(36), ForeignKey("users.id"), nullable=False),
            Column("password_hash", String(255), nullable=False),
            Column(
                "created_at",
                DateTime(timezone=True),
                server_default=text("now()"),
                nullable=False,
            ),
        )
    else:
        existing = {
            column["name"]
            for column in inspector.get_columns("password_history")
        }
        required = {"id", "user_id", "password_hash", "created_at"}
        missing = required - existing

        if missing:
            raise RuntimeError(
                f"Existing password_history table is missing columns: {sorted(missing)}"
            )

    indexes = {
        index["name"]
        for index in sa.inspect(op.get_bind()).get_indexes("password_history")
    }

    if "ix_password_history_user_id" not in indexes:
        op.create_index(
            "ix_password_history_user_id",
            "password_history",
            ["user_id"],
        )


def downgrade():
    raise RuntimeError(
        "This migration is intentionally irreversible to protect password history."
    )
