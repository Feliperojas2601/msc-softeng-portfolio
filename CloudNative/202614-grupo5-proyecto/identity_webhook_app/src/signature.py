import hashlib


def build_verify_token(secret_token: str, ruv: str, score: float) -> str:
    """Compute the SHA256 signature TrueNative sends as verifyToken."""
    raw = f"{secret_token}:{ruv}:{score}"
    return hashlib.sha256(raw.encode()).hexdigest()


def is_signature_valid(
    secret_token: str, ruv: str, score: float, verify_token: str
) -> bool:
    """Check whether verify_token matches the expected TrueNative signature."""
    return build_verify_token(secret_token, ruv, score) == verify_token
