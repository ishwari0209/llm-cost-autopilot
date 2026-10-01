
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.models import LLMModel, LLMRequest, RoutingDecision, User
from app.db.session import get_db
from app.providers.gemini import GeminiProvider
from app.router.complexity import score_prompt
from app.router.llm_classifier import classify_prompt
from app.router.selector import select_model
from app.services.budget import get_budget_status
from app.services.cost import calculate_cost
from app.services.rate_limit import check_rate_limit
from app.services.usage import track_usage

router = APIRouter(prefix="/v1", tags=["chat"])
provider = GeminiProvider()


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1)
    model: str | None = None
    router_type: str = "llm"


class ChatResponse(BaseModel):
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost: float
    complexity_score: int | None = None
    complexity_level: str | None = None
    routing_reason: str | None = None
    fallback: bool = False
    fallback_reason: str | None = None
    budget_tier: str | None = None
    budget_percent_used: float | None = None


@router.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Rate limiting
    allowed, remaining = check_rate_limit(current_user.id)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
        )

    # 2. Budget check
    # NOTE: Update the budget service to be user-specific before
    # relying on this for per-user budget enforcement.
    budget = get_budget_status(current_user.id)

    if budget.tier == "blocked":
        raise HTTPException(
            status_code=402,
            detail=(
                f"Monthly budget of ${budget.limit:.2f} exceeded "
                f"(spent ${budget.spent:.4f}). "
                "Requests are blocked until next month."
            ),
        )

    # 3. Select model
    routing_info = None

    if not req.model or req.model == "auto":
        if req.router_type == "llm":
            routing_info = classify_prompt(req.prompt)
        else:
            routing_info = score_prompt(req.prompt)

        if budget.tier == "restricted":
            model_name = "gemini-3.5-flash-lite"
        else:
            model_name = select_model(routing_info.level)
    else:
        model_name = req.model

    # 4. Find selected model
    model_row = (
        db.query(LLMModel)
        .filter_by(model_name=model_name, active=True)
        .first()
    )

    if not model_row:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' is not in the models table.",
        )

    # 5. Generate response, with fallback when applicable
    fallback_used = False
    fallback_reason = None

    try:
        result = provider.generate(req.prompt, model_name)

    except Exception as e:
        error_text = str(e)

        should_fallback = (
            model_name == "gemini-3.6-flash"
            and (
                ("429" in error_text and "RESOURCE_EXHAUSTED" in error_text)
                or ("503" in error_text and "UNAVAILABLE" in error_text)
            )
        )

        if should_fallback:
            fallback_model = "gemini-3.5-flash-lite"

            fallback_row = (
                db.query(LLMModel)
                .filter_by(model_name=fallback_model, active=True)
                .first()
            )

            if not fallback_row:
                raise HTTPException(
                    status_code=502,
                    detail=f"Fallback model '{fallback_model}' is not available.",
                )

            try:
                result = provider.generate(req.prompt, fallback_model)
                model_name = fallback_model
                model_row = fallback_row
                fallback_used = True
                fallback_reason = (
                    "strong_model_quota_exceeded"
                    if "429" in error_text
                    else "strong_model_overloaded"
                )

            except Exception as fallback_error:
                failed_request = LLMRequest(
                    user_id=current_user.id,
                    model_id=model_row.id,
                    prompt=req.prompt,
                    status="error",
                    error=str(fallback_error),
                )
                db.add(failed_request)
                db.commit()

                raise HTTPException(
                    status_code=502,
                    detail=f"LLM provider error: {fallback_error}",
                ) from fallback_error

        else:
            failed_request = LLMRequest(
                user_id=current_user.id,
                model_id=model_row.id,
                prompt=req.prompt,
                status="error",
                error=error_text,
            )
            db.add(failed_request)
            db.commit()

            raise HTTPException(
                status_code=502,
                detail=f"LLM provider error: {error_text}",
            ) from e

    # 6. Calculate cost and tokens
    cost = calculate_cost(
        result.input_tokens,
        result.output_tokens,
        model_row.input_price_per_1m,
        model_row.output_price_per_1m,
    )
    total_tokens = result.input_tokens + result.output_tokens

    # 7. Save successful request
    saved_request = LLMRequest(
        user_id=current_user.id,
        model_id=model_row.id,
        prompt=req.prompt,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        latency_ms=result.latency_ms,
        cost=cost,
        status="success",
    )
    db.add(saved_request)
    db.flush()

    # 8. Track usage for this user
    track_usage(
        user_id=current_user.id,
        tokens=total_tokens,
        cost=cost,
    )

    # 9. Save routing decision
    if routing_info:
        db.add(
            RoutingDecision(
                request_id=saved_request.id,
                complexity_score=routing_info.score,
                complexity_level=routing_info.level,
                selected_model=model_name,
                reason="; ".join(routing_info.reasons),
            )
        )

    db.commit()

    # 10. Prepare response
    response_data = result.__dict__ | {
        "cost": float(cost),
        "fallback": fallback_used,
        "fallback_reason": fallback_reason,
    }

    if routing_info:
        response_data.update(
            {
                "complexity_score": routing_info.score,
                "complexity_level": routing_info.level,
                "routing_reason": "; ".join(routing_info.reasons),
            }
        )

    response_data["budget_tier"] = budget.tier
    response_data["budget_percent_used"] = round(budget.percent_used, 1)

    return ChatResponse(**response_data)