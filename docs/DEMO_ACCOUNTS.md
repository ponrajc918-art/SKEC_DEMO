# Development demo accounts

These accounts are created only by the local development seed. They use synthetic records and the shared password `DemoPass!2026`; replace or disable them outside a local development environment.

| Role | Email |
|---|---|
| Student | `student.demo@skec.example` |
| Faculty | `faculty.demo@skec.example` |
| HOD | `hod.demo@skec.example` |
| Principal | `principal.demo@skec.example` |
| College Administrator | `admin.demo@skec.example` |

Additional synthetic student accounts are included for roster demonstrations: `student2.demo@skec.example` through `student4.demo@skec.example`. All development accounts use the shared demo password and are marked `must_change_password`.

The application forces a password-change flag on these accounts. MFA policy and a reset-email adapter are architecture hooks only until approved delivery credentials and an institutional identity process are supplied.
