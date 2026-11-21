# Role and permission matrix

This is the **implemented** matrix, not the broader target matrix from the brief. Protected write and administrative endpoints use database-backed `role_permissions`; ownership and department checks remain separate and mandatory.

| Role | Current permissions / scope |
|---|---|
| `student` | Own invoices/payment order and verification, own assignment submission/upload, own leave request; existing read endpoints retain student ownership filtering. |
| `staff` | Attendance and assignments for assigned offerings, assigned teaching workload, scoped student list, draft result entry. |
| `hod` | Staff capabilities plus result publication, notices and administrative summary. Existing academic scope must still be tightened for reports. |
| `principal` | Draft/publish results, notices and administrative summary. |
| `college_admin` | User list, student creation, invitations, notices, summary, audit permission and result publication. |
| `super_admin` | Catalogue grants all current capabilities, but a missing student/staff record now results in an explicit scope denial rather than a handler error. Dedicated super-admin workflows are absent. |
| `exam_staff` | Draft and publish result permissions are provisioned; dedicated exam workflows and question-paper controls are absent. |
| `accounts_staff` | Accounts-report permission is provisioned; reports and invoice administration are absent. |

Permission definitions live in `backend/app/permissions.py`; migration `0005_permission_catalogue` provisions roles, permissions and mappings idempotently. UI visibility is never authorization.
