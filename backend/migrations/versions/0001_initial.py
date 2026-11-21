"""initial schema

Revision ID: 0001_initial
Revises:
"""
from alembic import op
from sqlalchemy import MetaData
from app.models import Base
revision="0001_initial";down_revision=None;branch_labels=None;depends_on=None
INITIAL_TABLES=("users","roles","permissions","role_permissions","user_roles","sessions","departments","students","staff","subject_offerings","attendance_sessions","attendance_records","assignments","results","invoices","circulars","enquiries","audit_logs")
def upgrade():
    # This migration predates account-verification additions. Clone the historical
    # table set and remove later columns so ORM changes cannot alter revision 1.
    historical = MetaData()
    tables = [Base.metadata.tables[name].to_metadata(historical) for name in INITIAL_TABLES]
    users = historical.tables["users"]
    for name in (
        "email_verified_at",
        "last_login_at",
        "mobile_number",
        "mobile_verified_at",
    ):
        if name in users.c:
            for index in list(users.indexes):
                if name in index.columns.keys():
                    users.indexes.remove(index)
            users._columns.remove(users.c[name])
    historical.create_all(bind=op.get_bind(), tables=tables)
def downgrade():
    Base.metadata.drop_all(bind=op.get_bind(),tables=[Base.metadata.tables[name] for name in reversed(INITIAL_TABLES)])
