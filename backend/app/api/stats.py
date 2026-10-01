
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.models import LLMModel, LLMRequest, RoutingDecision, User
from app.db.session import get_db

router = APIRouter(prefix="/v1/stats", tags=["stats"])


@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requests = db.query(LLMRequest).filter(
        LLMRequest.user_id == current_user.id
    )

    total_requests = requests.count()
    total_tokens = requests.with_entities(
        func.sum(LLMRequest.input_tokens + LLMRequest.output_tokens)
    ).scalar() or 0
    total_cost = requests.with_entities(
        func.sum(LLMRequest.cost)
    ).scalar() or 0
    avg_latency = requests.filter(
        LLMRequest.status == "success"
    ).with_entities(func.avg(LLMRequest.latency_ms)).scalar() or 0

    return {
        "total_requests": total_requests,
        "total_tokens": int(total_tokens),
        "total_cost": float(total_cost),
        "avg_latency_ms": round(float(avg_latency), 1),
    }


@router.get("/model-usage")
def model_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(
            LLMModel.model_name,
            func.count(LLMRequest.id).label("count"),
        )
        .join(LLMRequest, LLMRequest.model_id == LLMModel.id)
        .filter(LLMRequest.user_id == current_user.id)
        .group_by(LLMModel.model_name)
        .all()
    )
    return [{"model": r.model_name, "count": r.count} for r in rows]


@router.get("/cost-over-time")
def cost_over_time(
    days: int = Query(default=14, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    since = date.today() - timedelta(days=days)
    rows = (
        db.query(
            func.date(LLMRequest.created_at).label("day"),
            func.sum(LLMRequest.cost).label("cost"),
        )
        .filter(
            LLMRequest.user_id == current_user.id,
            func.date(LLMRequest.created_at) >= since,
        )
        .group_by(func.date(LLMRequest.created_at))
        .order_by(func.date(LLMRequest.created_at))
        .all()
    )
    return [{"date": str(r.day), "cost": float(r.cost)} for r in rows]


@router.get("/requests")
def recent_requests(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(LLMRequest, LLMModel.model_name)
        .join(LLMModel, LLMRequest.model_id == LLMModel.id)
        .filter(LLMRequest.user_id == current_user.id)
        .order_by(LLMRequest.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.LLMRequest.id,
            "model": r.model_name,
            "input_tokens": r.LLMRequest.input_tokens,
            "output_tokens": r.LLMRequest.output_tokens,
            "latency_ms": r.LLMRequest.latency_ms,
            "cost": float(r.LLMRequest.cost),
            "status": r.LLMRequest.status,
            "created_at": r.LLMRequest.created_at.isoformat(),
        }
        for r in rows
    ]


@router.get("/routing-decisions")
def routing_decisions(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(RoutingDecision, LLMRequest.prompt)
        .join(LLMRequest, RoutingDecision.request_id == LLMRequest.id)
        .filter(LLMRequest.user_id == current_user.id)
        .order_by(RoutingDecision.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.RoutingDecision.id,
            "prompt": r.prompt[:100],
            "complexity_score": r.RoutingDecision.complexity_score,
            "complexity_level": r.RoutingDecision.complexity_level,
            "selected_model": r.RoutingDecision.selected_model,
            "reason": r.RoutingDecision.reason,
            "created_at": r.RoutingDecision.created_at.isoformat(),
        }
        for r in rows
    ]


@router.get("/models")
def list_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = db.query(LLMModel).filter_by(active=True).all()
    return [
        {
            "id": m.id,
            "provider": m.provider,
            "model_name": m.model_name,
            "input_price_per_1m": float(m.input_price_per_1m),
            "output_price_per_1m": float(m.output_price_per_1m),
        }
        for m in rows
    ]