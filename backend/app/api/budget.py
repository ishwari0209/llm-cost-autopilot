
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.budget import (
    get_budget_status,
    get_warning_threshold,
    get_restricted_threshold,
    set_monthly_budget,
    set_warning_threshold,
    set_restricted_threshold,
)

router = APIRouter(prefix="/v1", tags=["budget"])


class BudgetLimitRequest(BaseModel):
    amount: float = Field(gt=0, le=1_000_000)


class ThresholdRequest(BaseModel):
    percent: float = Field(gt=0, lt=100)


@router.get("/budget")
def budget_status():
    status = get_budget_status()

    return {
        "spent": round(status.spent, 4),
        "limit": status.limit,
        "percent_used": round(status.percent_used, 1),
        "tier": status.tier,
        "warning_threshold": status.warning_threshold,
        "restricted_threshold": status.restricted_threshold,
    }


@router.put("/budget/limit")
def update_budget(request: BudgetLimitRequest):
    set_monthly_budget(request.amount)
    status = get_budget_status()

    return {
        "message": "Monthly budget updated",
        "limit": status.limit,
        "spent": round(status.spent, 4),
        "percent_used": round(status.percent_used, 1),
        "tier": status.tier,
    }


@router.put("/budget/warning-threshold")
def update_warning_threshold(request: ThresholdRequest):
    if request.percent >= get_restricted_threshold():
        raise HTTPException(
            status_code=400,
            detail="Warning threshold must be lower than restricted threshold.",
        )

    set_warning_threshold(request.percent)

    return {
        "message": "Warning threshold updated",
        "warning_threshold": request.percent,
    }


@router.put("/budget/restricted-threshold")
def update_restricted_threshold(request: ThresholdRequest):
    if request.percent <= get_warning_threshold():
        raise HTTPException(
            status_code=400,
            detail="Restricted threshold must be higher than warning threshold.",
        )

    set_restricted_threshold(request.percent)

    return {
        "message": "Restricted threshold updated",
        "restricted_threshold": request.percent,
    }