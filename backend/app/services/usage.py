
from datetime import date

from app.core.redis_client import redis_client


def _month_key() -> str:
    return date.today().strftime("%Y-%m")


def track_usage(user_id: int, tokens: int, cost: float):
    today = date.today().isoformat()
    month = _month_key()
    prefix = f"usage:user:{user_id}"

    redis_client.incrby(f"{prefix}:requests:{today}", 1)
    redis_client.incrby(f"{prefix}:tokens:{today}", tokens)
    redis_client.incrbyfloat(f"{prefix}:cost:{today}", float(cost))

    redis_client.incrby(f"{prefix}:requests:month:{month}", 1)
    redis_client.incrbyfloat(
    f"{prefix}:cost:month:{month}",
    float(cost)
)


def get_today_usage(user_id: int) -> dict:
    today = date.today().isoformat()
    prefix = f"usage:user:{user_id}"

    return {
        "requests_today": int(
            redis_client.get(f"{prefix}:requests:{today}") or 0
        ),
        "tokens_today": int(
            redis_client.get(f"{prefix}:tokens:{today}") or 0
        ),
        "cost_today": float(
            redis_client.get(f"{prefix}:cost:{today}") or 0
        ),
    }


def get_month_cost(user_id: int) -> float:
    month = _month_key()
    key = f"usage:user:{user_id}:cost:month:{month}"
    return float(redis_client.get(key) or 0)