"""identity delivery payment and private file services

Revision ID: 0003_live_services
Revises: 0002_demo_workflows
"""
from alembic import op
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, text

revision="0003_live_services"
down_revision="0002_demo_workflows"
branch_labels=None
depends_on=None

def timestamps():return [Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False),Column("updated_at",DateTime(timezone=True),server_default=text("now()"),nullable=False)]
def upgrade():
    op.add_column("users",Column("email_verified_at",DateTime(timezone=True),nullable=True));op.add_column("users",Column("last_login_at",DateTime(timezone=True),nullable=True))
    op.create_table("password_reset_tokens",Column("id",String(36),primary_key=True),Column("user_id",String(36),ForeignKey("users.id"),nullable=False),Column("token_hash",String(64),nullable=False,unique=True),Column("purpose",String(30),nullable=False),Column("expires_at",DateTime(timezone=True),nullable=False),Column("used_at",DateTime(timezone=True),nullable=True),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False));op.create_index("ix_password_reset_tokens_user_id","password_reset_tokens",["user_id"])
    op.create_table("invitations",Column("id",String(36),primary_key=True),Column("user_id",String(36),ForeignKey("users.id"),nullable=False),Column("token_hash",String(64),nullable=False,unique=True),Column("expires_at",DateTime(timezone=True),nullable=False),Column("accepted_at",DateTime(timezone=True),nullable=True),Column("invited_by",String(36),ForeignKey("users.id"),nullable=False),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False));op.create_index("ix_invitations_user_id","invitations",["user_id"])
    op.create_table("mfa_factors",Column("id",String(36),primary_key=True),Column("user_id",String(36),ForeignKey("users.id"),nullable=False,unique=True),Column("secret_encrypted",Text,nullable=False),Column("confirmed_at",DateTime(timezone=True),nullable=True),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False))
    op.create_table("login_attempts",Column("id",String(36),primary_key=True),Column("identifier",String(255),nullable=False),Column("ip",String(64),nullable=False),Column("success",Boolean,nullable=False),Column("attempted_at",DateTime(timezone=True),server_default=text("now()"),nullable=False));op.create_index("ix_login_attempts_identifier","login_attempts",["identifier"]);op.create_index("ix_login_attempts_attempted_at","login_attempts",["attempted_at"])
    op.create_table("payments",Column("id",String(36),primary_key=True),Column("invoice_id",String(36),ForeignKey("invoices.id"),nullable=False),Column("amount_paise",Integer,nullable=False),Column("currency",String(3),nullable=False),Column("status",String(20),nullable=False),Column("gateway",String(30),nullable=False),Column("gateway_order_id",String(120),nullable=True,unique=True),Column("gateway_payment_id",String(120),nullable=True,unique=True),Column("idempotency_key",String(80),nullable=False,unique=True),Column("paid_at",DateTime(timezone=True),nullable=True),*timestamps());op.create_index("ix_payments_invoice_id","payments",["invoice_id"])
    op.create_table("payment_gateway_events",Column("id",String(36),primary_key=True),Column("gateway_event_id",String(120),nullable=True,unique=True),Column("signature_valid",Boolean,nullable=False),Column("event_type",String(100),nullable=False),Column("payload",JSON,nullable=False),Column("processed_at",DateTime(timezone=True),nullable=True),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False))
    op.create_table("email_deliveries",Column("id",String(36),primary_key=True),Column("user_id",String(36),ForeignKey("users.id"),nullable=True),Column("recipient",String(255),nullable=False),Column("template",String(80),nullable=False),Column("status",String(20),nullable=False),Column("provider_message_id",String(255),nullable=True),Column("error",String(500),nullable=True),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False))
    op.create_table("file_objects",Column("id",String(36),primary_key=True),Column("storage_key",String(255),nullable=False,unique=True),Column("original_name",String(255),nullable=False),Column("content_type",String(120),nullable=False),Column("size",Integer,nullable=False),Column("sha256",String(64),nullable=False),Column("scan_status",String(20),nullable=False),Column("visibility",String(20),nullable=False),Column("uploaded_by",String(36),ForeignKey("users.id"),nullable=False),Column("owner_student_id",String(36),ForeignKey("students.id"),nullable=True),*timestamps())
def downgrade():
    for table in ["file_objects","email_deliveries","payment_gateway_events","payments","login_attempts","mfa_factors","invitations","password_reset_tokens"]:op.drop_table(table)
    op.drop_column("users","last_login_at");op.drop_column("users","email_verified_at")
