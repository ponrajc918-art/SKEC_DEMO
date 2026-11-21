"""central role and permission catalogue

Revision ID: 0005_permission_catalogue
Revises: 0004_verification_mfa_recovery
"""
from alembic import op
from uuid import NAMESPACE_URL, uuid5

from app.permissions import PERMISSION_DESCRIPTIONS, ROLE_NAMES, ROLE_PERMISSIONS


revision = "0005_permission_catalogue"
down_revision = "0004_verification_mfa_recovery"
branch_labels = None
depends_on = None


def upgrade():
    def quoted(value: str) -> str:
        return "'" + value.replace("'", "''") + "'"

    for code, name in ROLE_NAMES.items():
        role_id = str(uuid5(NAMESPACE_URL, f"skec:role:{code}"))
        op.execute(
            "INSERT INTO roles (id, code, name) "
            f"SELECT {quoted(role_id)}, {quoted(code)}, {quoted(name)} "
            f"WHERE NOT EXISTS (SELECT 1 FROM roles WHERE code = {quoted(code)})"
        )
    for code, description in PERMISSION_DESCRIPTIONS.items():
        permission_id = str(uuid5(NAMESPACE_URL, f"skec:permission:{code}"))
        op.execute(
            "INSERT INTO permissions (id, code, description) "
            f"SELECT {quoted(permission_id)}, {quoted(code)}, {quoted(description)} "
            f"WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE code = {quoted(code)})"
        )
    for role_code, permission_codes in ROLE_PERMISSIONS.items():
        for permission_code in permission_codes:
            op.execute(
                "INSERT INTO role_permissions (role_id, permission_id) "
                "SELECT roles.id, permissions.id FROM roles, permissions "
                f"WHERE roles.code = {quoted(role_code)} AND permissions.code = {quoted(permission_code)} "
                "AND NOT EXISTS (SELECT 1 FROM role_permissions rp "
                "WHERE rp.role_id = roles.id AND rp.permission_id = permissions.id)"
            )


def downgrade():
    # Existing user-role assignments must never be removed by a downgrade.
    # The catalogue is therefore intentionally retained as harmless reference data.
    pass
