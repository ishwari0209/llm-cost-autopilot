
from dataclasses import dataclass

from app.core.redis_client import redis_client
from app.services.usage import get_month_cost

DEFAULT_BUDGET = 5.00
DEFAULT_WARNING_THRESHOLD = 80.0
DEFAULT_RESTRICTED_THRESHOLD = 90.0


def _budget_key(user_id: int) -> str:
    return f"config:user:{user_id}:monthly_budget"


def _warning_key(user_id: int) -> str:
    return f"config:user:{user_id}:warning_threshold"


def _restricted_key(user_id: int) -> str:
    return f"config:user:{user_id}:restricted_threshold"


def get_monthly_budget(user_id: int) -> float:
    value = redis_client.get(_budget_key(user_id))
    return float(value) if value else DEFAULT_BUDGET


def get_warning_threshold(user_id: int) -> float:
    value = redis_client.get(_warning_key(user_id))
    return float(value) if value else DEFAULT_WARNING_THRESHOLD


def get_restricted_threshold(user_id: int) -> float:
    value = redis_client.get(_restricted_key(user_id))
    return float(value) if value else DEFAULT_RESTRICTED_THRESHOLD


def set_monthly_budget(user_id: int, amount: float):
    redis_client.set(_budget_key(user_id), amount)


def set_warning_threshold(user_id: int, percent: float):
    redis_client.set(_warning_key(user_id), percent)


def set_restricted_threshold(user_id: int, percent: float):
    redis_client.set(_restricted_key(user_id), percent)


@dataclass
class BudgetStatus:
    spent: float
    limit: float
    percent_used: float
    tier: str
    warning_threshold: float
    restricted_threshold: float


def get_budget_status(user_id: int) -> BudgetStatus:
    spent = get_month_cost(user_id)
    limit = get_monthly_budget(user_id)
    warning_at = get_warning_threshold(user_id)
    restricted_at = get_restricted_threshold(user_id)

    percent = (spent / limit * 100) if limit > 0 else 0

    if percent >= 100:
        tier = "blocked"
    elif percent >= restricted_at:
        tier = "restricted"
    elif percent >= warning_at:
        tier = "warning"
    else:
        tier = "normal"

    return BudgetStatus(
        spent=spent,
        limit=limit,
        percent_used=percent,
        tier=tier,
        warning_threshold=warning_at,
        restricted_threshold=restricted_at,
    )