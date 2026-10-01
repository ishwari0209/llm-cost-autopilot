
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.auth import get_current_user
from app.db.models import User
from app.services.budget import (
    get_budget_status,
    get_monthly_budget,
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
def budget_status(
    current_user: User = Depends(get_current_user),
):
    status = get_budget_status(current_user.id)

    return {
        "spent": round(status.spent, 4),
        "limit": status.limit,
        "percent_used": round(status.percent_used, 1),
        "tier": status.tier,
        "warning_threshold": status.warning_threshold,
        "restricted_threshold": status.restricted_threshold,
    }


@router.put("/budget/limit")
def update_budget(
    request: BudgetLimitRequest,
    current_user: User = Depends(get_current_user),
):
    set_monthly_budget(current_user.id, request.amount)
    status = get_budget_status(current_user.id)

    return {
        "message": "Monthly budget updated",
        "limit": status.limit,
        "spent": round(status.spent, 4),
        "percent_used": round(status.percent_used, 1),
        "tier": status.tier,
    }


@router.put("/budget/warning-threshold")
def update_warning_threshold(
    request: ThresholdRequest,
    current_user: User = Depends(get_current_user),
):
    restricted = get_restricted_threshold(current_user.id)

    if request.percent >= restricted:
        raise HTTPException(
            status_code=400,
            detail="Warning threshold must be lower than restricted threshold.",
        )

    set_warning_threshold(current_user.id, request.percent)

    return {
        "message": "Warning threshold updated",
        "warning_threshold": request.percent,
    }


@router.put("/budget/restricted-threshold")
def update_restricted_threshold(
    request: ThresholdRequest,
    current_user: User = Depends(get_current_user),
):
    warning = get_warning_threshold(current_user.id)

    if request.percent <= warning:
        raise HTTPException(
            status_code=400,
            detail="Restricted threshold must be higher than warning threshold.",
        )

    set_restricted_threshold(current_user.id, request.percent)

    return {
        "message": "Restricted threshold updated",
        "restricted_threshold": request.percent,
    }