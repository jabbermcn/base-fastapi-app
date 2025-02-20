from datetime import UTC, datetime, timezone


__all__ = ["now"]


def now(tz: timezone = None) -> datetime:
    if tz is None:
        tz = UTC

    return datetime.now(tz=tz)
