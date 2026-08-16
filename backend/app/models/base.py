from datetime import UTC, datetime


def get_datetime_utc() -> datetime:
    """Timezone-aware UTC now, used as the default for created_at columns."""
    return datetime.now(UTC)
