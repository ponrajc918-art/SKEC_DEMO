"""demo workflow tables

Revision ID: 0002_demo_workflows
Revises: 0001_initial
"""
from alembic import op
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, text

revision="0002_demo_workflows"
down_revision="0001_initial"
branch_labels=None
depends_on=None

def upgrade():
    timestamps=[Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False),Column("updated_at",DateTime(timezone=True),server_default=text("now()"),nullable=False)]
    op.create_table("assignment_submissions",Column("id",String(36),primary_key=True),Column("assignment_id",String(36),ForeignKey("assignments.id"),nullable=False),Column("student_id",String(36),ForeignKey("students.id"),nullable=False),Column("note",Text,nullable=False),Column("status",String(20),nullable=False),Column("marks",Integer,nullable=True),Column("feedback",Text,nullable=True),*timestamps,UniqueConstraint("assignment_id","student_id"))
    op.create_table("timetable_entries",Column("id",String(36),primary_key=True),Column("offering_id",String(36),ForeignKey("subject_offerings.id"),nullable=False),Column("day_of_week",String(12),nullable=False),Column("period",Integer,nullable=False),Column("room",String(60),nullable=False),Column("starts_at",String(10),nullable=False),Column("ends_at",String(10),nullable=False),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False),Column("updated_at",DateTime(timezone=True),server_default=text("now()"),nullable=False))
    op.create_table("notifications",Column("id",String(36),primary_key=True),Column("user_id",String(36),ForeignKey("users.id"),nullable=False),Column("title",String(200),nullable=False),Column("body",Text,nullable=False),Column("kind",String(40),nullable=False),Column("read_at",DateTime(timezone=True),nullable=True),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False),Column("updated_at",DateTime(timezone=True),server_default=text("now()"),nullable=False))
    op.create_table("leave_requests",Column("id",String(36),primary_key=True),Column("student_id",String(36),ForeignKey("students.id"),nullable=False),Column("from_date",Date,nullable=False),Column("to_date",Date,nullable=False),Column("reason",Text,nullable=False),Column("status",String(20),nullable=False),Column("created_at",DateTime(timezone=True),server_default=text("now()"),nullable=False),Column("updated_at",DateTime(timezone=True),server_default=text("now()"),nullable=False))
def downgrade():
    op.drop_table("leave_requests");op.drop_table("notifications");op.drop_table("timetable_entries");op.drop_table("assignment_submissions")
