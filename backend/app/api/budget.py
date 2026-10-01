from fastapi import APIRouter

from app.services.budget import get_budget_status

router = APIRouter(prefix="/v1", tags=["budget"])


@router.get("/budget")
def budget_status():
    status = get_budget_status()
    return {
        "spent": round(status.spent, 4),
        "limit": status.limit,
        "percent_used": round(status.percent_used, 1),
        "tier": status.tier,
    }