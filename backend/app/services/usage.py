from datetime import date

from app.core.redis_client import redis_client


def track_usage(tokens: int, cost: float):
    today = date.today().isoformat()
    redis_client.incrby(f"usage:requests:{today}", 1)
    redis_client.incrby(f"usage:tokens:{today}", tokens)
    redis_client.incrbyfloat(f"usage:cost:{today}", cost)


def get_today_usage() -> dict:
    today = date.today().isoformat()
    return {
        "requests_today": int(redis_client.get(f"usage:requests:{today}") or 0),
        "tokens_today": int(redis_client.get(f"usage:tokens:{today}") or 0),
        "cost_today": float(redis_client.get(f"usage:cost:{today}") or 0),
    }