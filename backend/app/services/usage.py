from datetime import date

from app.core.redis_client import redis_client


def _month_key() -> str:
    return date.today().strftime("%Y-%m")


def track_usage(tokens: int, cost: float):
    today = date.today().isoformat()
    month = _month_key()

    redis_client.incrby(f"usage:requests:{today}", 1)
    redis_client.incrby(f"usage:tokens:{today}", tokens)
    redis_client.incrbyfloat(f"usage:cost:{today}", cost)

    redis_client.incrby(f"usage:requests:month:{month}", 1)
    redis_client.incrbyfloat(f"usage:cost:month:{month}", cost)


def get_today_usage() -> dict:
    today = date.today().isoformat()
    return {
        "requests_today": int(redis_client.get(f"usage:requests:{today}") or 0),
        "tokens_today": int(redis_client.get(f"usage:tokens:{today}") or 0),
        "cost_today": float(redis_client.get(f"usage:cost:{today}") or 0),
    }


def get_month_cost() -> float:
    month = _month_key()
    return float(redis_client.get(f"usage:cost:month:{month}") or 0)