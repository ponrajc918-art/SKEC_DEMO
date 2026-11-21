"""Central, database-backed authorization catalogue.

Roles are assigned to users in ``user_roles`` and their capabilities are assigned
through ``role_permissions``.  Endpoint handlers must still apply ownership and
department checks; a permission is never a substitute for resource scope.
"""
from __future__ import annotations

PERMISSION_DESCRIPTIONS = {
    "academic.attendance.write": "Record attendance for an assigned subject",
    "academic.assignments.write": "Create assignments for an assigned subject",
    "academic.students.read": "View students within an authorised academic scope",
    "academic.teaching.read": "View assigned teaching workload",
    "announcements.publish": "Publish circulars and announcements",
    "admin.dashboard.read": "View administrative summary data",
    "admin.students.create": "Create student accounts",
    "admin.users.invite": "Issue account invitations",
    "admin.users.read": "View user accounts",
    "audit.read": "View audit records",
    "exams.results.publish": "Publish approved results",
    "exams.results.write": "Enter draft results",
    "files.upload_own": "Upload a personal assignment file",
    "finance.invoices.read_own": "View own fee invoices",
    "finance.reports.read": "View accounts reports",
    "finance.payments.create_own": "Create payment orders for own invoices",
    "finance.payments.verify_own": "Submit own payment verification data",
    "student.assignments.submit_own": "Submit own assignments",
    "student.leave.create_own": "Create own leave requests",
}

ROLE_PERMISSIONS = {
    "student": {
        "finance.invoices.read_own", "finance.payments.create_own",
        "finance.payments.verify_own", "files.upload_own",
        "student.assignments.submit_own", "student.leave.create_own",
    },
    "staff": {
        "academic.attendance.write", "academic.assignments.write",
        "academic.students.read", "academic.teaching.read", "exams.results.write",
    },
    "hod": {
        "academic.attendance.write", "academic.assignments.write",
        "academic.students.read", "academic.teaching.read", "announcements.publish",
        "admin.dashboard.read", "exams.results.publish", "exams.results.write",
    },
    "principal": {
        "admin.dashboard.read", "announcements.publish", "exams.results.publish",
        "exams.results.write",
    },
    "college_admin": {
        "admin.dashboard.read", "admin.students.create", "admin.users.invite",
        "admin.users.read", "announcements.publish", "audit.read",
        "exams.results.publish",
    },
    "super_admin": set(PERMISSION_DESCRIPTIONS),
    "exam_staff": {"exams.results.publish", "exams.results.write"},
    "accounts_staff": {"finance.reports.read"},
}

ROLE_NAMES = {
    "student": "Student", "staff": "Faculty", "hod": "HOD",
    "principal": "Principal", "college_admin": "College Admin",
    "super_admin": "Super Admin", "exam_staff": "Exam Staff",
    "accounts_staff": "Accounts Staff",
}
