
import base64
import hmac
import json
import re
from hashlib import sha256
from urllib.request import Request, urlopen

from .core import settings


_SIGNATURE_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")


def enabled() -> bool:
    cfg = settings()
    return (
        bool(cfg.razorpay_key_id and cfg.razorpay_key_secret)
        and cfg.payment_mode in {"test", "live"}
        and (cfg.payment_mode != "live" or cfg.allow_live_payments)
    )


def create_order(receipt: str, amount_paise: int, idempotency_key: str) -> dict:
    if not enabled():
        raise RuntimeError("Razorpay is not configured")

    if type(amount_paise) is not int or amount_paise <= 0:
        raise ValueError("Payment amount must be a positive integer in paise")

    if not isinstance(receipt, str) or not receipt.strip():
        raise ValueError("Payment receipt is required")

    if (
        not isinstance(idempotency_key, str)
        or not idempotency_key.strip()
        or len(idempotency_key) > 80
    ):
        raise ValueError("A valid idempotency key is required")

    cfg = settings()
    payload = json.dumps({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": receipt,
        "notes": {"idempotency_key": idempotency_key},
    }).encode()

    auth = base64.b64encode(
        f"{cfg.razorpay_key_id}:{cfg.razorpay_key_secret}".encode()
    ).decode()

    request = Request(
        "https://api.razorpay.com/v1/orders",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        },
    )

    with urlopen(request, timeout=15) as response:
        result = json.loads(response.read())

    if not isinstance(result, dict):
        raise RuntimeError("Invalid Razorpay order response")

    if (
        not isinstance(result.get("id"), str)
        or not result["id"].strip()
        or type(result.get("amount")) is not int
        or result["amount"] != amount_paise
        or result.get("currency") != "INR"
    ):
        raise RuntimeError("Razorpay order response failed validation")

    return result


def verify_payment_signature(
    order_id: str, payment_id: str, signature: str
) -> bool:
    secret = settings().razorpay_key_secret

    if not secret or not isinstance(signature, str):
        return False

    if not _SIGNATURE_PATTERN.fullmatch(signature):
        return False

    message = f"{order_id}|{payment_id}".encode()
    expected = hmac.new(secret.encode(), message, sha256).hexdigest()

    return hmac.compare_digest(expected, signature.lower())


def verify_webhook(raw: bytes, signature: str) -> bool:
    secret = settings().razorpay_webhook_secret

    if not secret or not isinstance(signature, str):
        return False

    if not _SIGNATURE_PATTERN.fullmatch(signature):
        return False

    expected = hmac.new(secret.encode(), raw, sha256).hexdigest()

    return hmac.compare_digest(expected, signature.lower())
