from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

def to_utc(dt: datetime):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)