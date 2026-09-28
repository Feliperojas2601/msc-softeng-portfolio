import uuid
from datetime import datetime, timedelta

from domain.services.token_service import (
    compute_expiration,
    generate_token,
    is_expired,
    utcnow,
)


def test_generate_token_returns_a_valid_uuid4_string():
    """The generated token must be a valid, unique UUID string."""
    token = generate_token()

    assert str(uuid.UUID(token)) == token
    assert token != generate_token()


def test_compute_expiration_is_hours_in_the_future():
    """compute_expiration returns a timestamp roughly N hours after now."""
    before = utcnow()
    expire_at = compute_expiration(24)
    after = utcnow()

    assert before + timedelta(hours=24) <= expire_at <= after + timedelta(hours=24)


def test_is_expired_returns_true_for_none():
    """A user without an expiration timestamp is considered expired."""
    assert is_expired(None) is True


def test_is_expired_returns_true_for_past_timestamp():
    """A timestamp in the past is expired."""
    assert is_expired(utcnow() - timedelta(hours=1)) is True


def test_is_expired_returns_false_for_future_timestamp():
    """A timestamp in the future is not expired."""
    assert is_expired(utcnow() + timedelta(hours=1)) is False


def test_utcnow_is_timezone_naive():
    """utcnow returns a naive datetime so it serializes without a UTC offset."""
    now = utcnow()

    assert isinstance(now, datetime)
    assert now.tzinfo is None
