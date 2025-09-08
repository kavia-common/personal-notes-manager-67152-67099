"""
Authentication utilities: password hashing and token generation/verification.

Uses werkzeug.security for password hashing and itsdangerous for token signing.
Tokens are simple signed payloads containing user_id and email.
"""
from __future__ import annotations
import os
import time
from typing import Optional, Dict, Any
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

DEFAULT_TOKEN_TTL_SECONDS = 60 * 60 * 24  # 24 hours


def _get_secret_key() -> str:
    # In production, this must be set via environment variable.
    secret = os.environ.get("SECRET_KEY")
    if not secret:
        # Safe default for development/CI; not suitable for production.
        secret = "dev-secret-key-change-me"
    return secret


def _get_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(_get_secret_key(), salt="notes-backend-auth")


# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Hash plain password for storage."""
    return generate_password_hash(password)


# PUBLIC_INTERFACE
def verify_password(password: str, password_hash: str) -> bool:
    """Verify plain password against stored hash."""
    return check_password_hash(password_hash, password)


# PUBLIC_INTERFACE
def create_access_token(user_id: str, email: str, ttl_seconds: Optional[int] = None) -> str:
    """
    Create a signed access token for a user.

    Args:
        user_id: The user's unique id.
        email: The user's email.
        ttl_seconds: Optional override for token TTL.

    Returns:
        Signed token string.
    """
    ttl = ttl_seconds or DEFAULT_TOKEN_TTL_SECONDS
    s = _get_serializer()
    payload = {"sub": user_id, "email": email, "iat": int(time.time())}
    return s.dumps(payload), ttl


# PUBLIC_INTERFACE
def verify_access_token(token: str, max_age: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """
    Verify a signed access token and return payload if valid, else None.

    Args:
        token: Signed token string.
        max_age: Optional token age limit in seconds.

    Returns:
        Payload dict or None.
    """
    s = _get_serializer()
    try:
        data = s.loads(token, max_age=max_age or DEFAULT_TOKEN_TTL_SECONDS)
        return data
    except SignatureExpired:
        return None
    except BadSignature:
        return None
