from dataclasses import dataclass

from app.core.config import settings
from app.services.usage import get_month_cost


@dataclass
class BudgetStatus:
    spent: float
    limit: float
    percent_used: float
    tier: str  # "normal", "warning", "restricted", "blocked"


def get_budget_status() -> BudgetStatus:
    spent = get_month_cost()
    limit = settings.monthly_budget
    percent = (spent / limit * 100) if limit > 0 else 0

    if percent >= 100:
        tier = "blocked"
    elif percent >= 90:
        tier = "restricted"
    elif percent >= 80:
        tier = "warning"
    else:
        tier = "normal"

    return BudgetStatus(spent=spent, limit=limit, percent_used=percent, tier=tier)