"""Fail-closed ClamAV daemon adapter for private uploads."""
from __future__ import annotations

import socket

from .core import settings


class ScannerUnavailable(RuntimeError):
    pass


def scan(data: bytes) -> str:
    """Return ``clean`` or ``rejected``. Raise when scanning cannot be performed."""
    cfg = settings()
    if cfg.file_scanner_mode != "clamd":
        raise ScannerUnavailable("Malware scanning is not configured")
    if not cfg.clamd_host:
        raise ScannerUnavailable("Malware scanning is not configured")
    try:
        with socket.create_connection((cfg.clamd_host, cfg.clamd_port), cfg.clamd_timeout_seconds) as conn:
            conn.settimeout(cfg.clamd_timeout_seconds)
            conn.sendall(b"zINSTREAM\0")
            for offset in range(0, len(data), 1024 * 1024):
                chunk = data[offset : offset + 1024 * 1024]
                conn.sendall(len(chunk).to_bytes(4, "big"))
                conn.sendall(chunk)
            conn.sendall((0).to_bytes(4, "big"))
            response = conn.recv(4096).decode("utf-8", "replace")
    except OSError as exc:
        raise ScannerUnavailable("Malware scanner is unavailable") from exc
    if response.endswith("OK\n"):
        return "clean"
    if "FOUND" in response:
        return "rejected"
    raise ScannerUnavailable("Malware scanner returned an invalid response")
