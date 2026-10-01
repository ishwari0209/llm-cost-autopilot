from datetime import datetime

from app.core.redis_client import redis_client

RATE_LIMIT_PER_HOUR = 3  # adjust as needed for your free-tier quota


def check_rate_limit(user_id: int) -> tuple[bool, int]:
    """Returns (allowed, remaining)."""
    hour_bucket = datetime.utcnow().strftime("%Y%m%d%H")
    key = f"rate_limit:{user_id}:{hour_bucket}"

    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, 3600)  # expire after 1 hour

    remaining = max(0, RATE_LIMIT_PER_HOUR - current)
    allowed = current <= RATE_LIMIT_PER_HOUR
    return allowed, remaining