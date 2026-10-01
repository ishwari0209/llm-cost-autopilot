from dataclasses import dataclass

from app.core.redis_client import redis_client
from app.services.usage import get_month_cost

DEFAULT_BUDGET = 5.00
DEFAULT_WARNING_THRESHOLD = 80.0
DEFAULT_RESTRICTED_THRESHOLD = 90.0

BUDGET_KEY = "config:monthly_budget"
WARNING_KEY = "config:warning_threshold"
RESTRICTED_KEY = "config:restricted_threshold"


def get_monthly_budget() -> float:
    value = redis_client.get(BUDGET_KEY)
    return float(value) if value else DEFAULT_BUDGET


def get_warning_threshold() -> float:
    value = redis_client.get(WARNING_KEY)
    return float(value) if value else DEFAULT_WARNING_THRESHOLD


def get_restricted_threshold() -> float:
    value = redis_client.get(RESTRICTED_KEY)
    return float(value) if value else DEFAULT_RESTRICTED_THRESHOLD


def set_monthly_budget(amount: float):
    redis_client.set(BUDGET_KEY, amount)


def set_warning_threshold(percent: float):
    redis_client.set(WARNING_KEY, percent)


def set_restricted_threshold(percent: float):
    redis_client.set(RESTRICTED_KEY, percent)


@dataclass
class BudgetStatus:
    spent: float
    limit: float
    percent_used: float
    tier: str
    warning_threshold: float
    restricted_threshold: float


def get_budget_status() -> BudgetStatus:
    spent = get_month_cost()
    limit = get_monthly_budget()
    warning_at = get_warning_threshold()
    restricted_at = get_restricted_threshold()
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
        spent=spent, limit=limit, percent_used=percent, tier=tier,
        warning_threshold=warning_at, restricted_threshold=restricted_at,
    )