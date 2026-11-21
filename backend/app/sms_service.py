"""Provider-neutral SMS delivery adapter.

The generic HTTP adapter deliberately makes no provider-specific delivery claim.
Deployments must configure the provider's approved endpoint and authenticate it with
an environment-provided bearer token.  With no provider configured, callers receive
an explicit unavailable result rather than a fabricated delivery.
"""
from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from .core import settings


class SmsUnavailable(RuntimeError):
    pass


def send_otp(destination: str, code: str) -> None:
    cfg = settings()
    if cfg.sms_provider != "generic_http":
        raise SmsUnavailable("SMS delivery is not configured")
    if not all([cfg.sms_endpoint, cfg.sms_api_token, cfg.sms_sender_id]):
        raise SmsUnavailable("SMS delivery is not configured")

    body = json.dumps(
        {
            "to": destination,
            "from": cfg.sms_sender_id,
            "message": f"Your SKEC Digital Campus verification code is {code}. It expires in {cfg.otp_expiry_minutes} minutes.",
        }
    ).encode("utf-8")
    request = Request(
        cfg.sms_endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {cfg.sms_api_token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=15) as response:
            if not 200 <= response.status < 300:
                raise SmsUnavailable("SMS provider rejected the request")
    except (URLError, TimeoutError, OSError) as exc:
        raise SmsUnavailable("SMS provider is unavailable") from exc
