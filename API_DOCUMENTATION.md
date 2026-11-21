# API documentation

Interactive OpenAPI documentation is available at `/api/docs` when the backend is running. The versioned schema is `/api/v1/openapi.json`.

Security uses the `skec_session` HTTP-only cookie plus the `skec_csrf` cookie/header pair. State-changing browser requests must send `X-CSRF-Token`; raw Razorpay webhooks use `X-Razorpay-Signature` instead.

Recent identity endpoints: `POST /api/v1/auth/email-verification/request`, `POST /api/v1/auth/email-verification/confirm`, `POST /api/v1/auth/mobile-verification/request`, `POST /api/v1/auth/mobile-verification/confirm`, and `POST /api/v1/auth/mfa/recovery-codes`. OTP values are never included in responses. SMS endpoint requests return `503 sms_unavailable` when no real provider is configured.

Assignment upload is `POST /api/v1/files/assignments/{assignment_id}` with raw permitted file bytes, `Content-Type` and `X-Filename`. The file remains unavailable unless ClamAV marks it clean; there is no administrative clean-status override.
