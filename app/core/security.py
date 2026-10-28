import hashlib
import hmac
import json
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode

from app.core.config import get_settings


def _b64encode(data: bytes) -> str:
    return urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    settings = get_settings()
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        settings.secret_key.encode(),
        120_000,
    ).hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(hash_password(plain_password), hashed_password)


def create_access_token(subject: str, expires_delta_seconds: int | None = None) -> str:
    settings = get_settings()
    exp = int(time.time()) + (
        expires_delta_seconds or settings.access_token_expire_minutes * 60
    )
    body = _b64encode(json.dumps({"sub": subject, "exp": exp}, separators=(",", ":")).encode())
    signature = hmac.new(settings.secret_key.encode(), body.encode(), hashlib.sha256).digest()
    return f"{body}.{_b64encode(signature)}"


def decode_access_token(token: str) -> str | None:
    settings = get_settings()
    try:
        body, signature = token.split(".", 1)
        expected = hmac.new(settings.secret_key.encode(), body.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64encode(expected), signature):
            return None
        payload = json.loads(_b64decode(body))
        if payload.get("exp", 0) < time.time():
            return None
        return payload.get("sub")
    except (ValueError, json.JSONDecodeError):
        return None
