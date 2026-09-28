import hashlib
import secrets

_ALGORITHM = "sha256"
_ITERATIONS = 100_000


def generate_salt() -> str:
    """Generate a new random salt."""
    return secrets.token_hex(16)


def hash_password(password: str, salt: str) -> str:
    """Hash a plain text password using the given salt."""
    derived_key = hashlib.pbkdf2_hmac(
        _ALGORITHM, password.encode("utf-8"), salt.encode("utf-8"), _ITERATIONS
    )
    return derived_key.hex()


def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    """Check whether a plain text password matches a stored hash."""
    return secrets.compare_digest(hash_password(password, salt), hashed_password)
