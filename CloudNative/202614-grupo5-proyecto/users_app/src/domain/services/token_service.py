import uuid
from datetime import datetime, timedelta, timezone


def generate_token() -> str:
    """Generate a new random session token."""
    return str(uuid.uuid4())


def compute_expiration(hours: int) -> datetime:
    """Compute the expiration timestamp for a new token, in UTC."""
    return utcnow() + timedelta(hours=hours)


def utcnow() -> datetime:
    """Return the current UTC timestamp, timezone-naive for ISO formatting."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def is_expired(expire_at: datetime | None) -> bool:
    """Check whether a token expiration timestamp is in the past."""
    return expire_at is None or expire_at < utcnow()
