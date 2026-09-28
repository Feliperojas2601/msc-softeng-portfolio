from datetime import datetime, timedelta, timezone

from entrypoints.api.schemas.credit_card_schemas import format_date


def test_dates_are_normalized_to_utc():
    local = datetime(2026, 1, 1, 23, 30, tzinfo=timezone(timedelta(hours=-5)))
    assert format_date(local) == "2026-01-02T04:30:00"
