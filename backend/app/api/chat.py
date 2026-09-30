from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import LLMModel, LLMRequest, RoutingDecision
from app.db.session import get_db
from app.providers.gemini import GeminiProvider
from app.router.complexity import score_prompt
from app.router.selector import select_model
from app.services.cost import calculate_cost

router = APIRouter(prefix="/v1", tags=["chat"])
provider = GeminiProvider()


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1)
    user_id: int = 1
    model: str | None = None  # None or "auto" => let the router decide


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


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    routing_info = None

    if not req.model or req.model == "auto":
        routing_info = score_prompt(req.prompt)
        model_name = select_model(routing_info.level)
    else:
        model_name = req.model

    model_row = db.query(LLMModel).filter_by(model_name=model_name, active=True).first()
    if not model_row:
        raise HTTPException(400, f"Model '{model_name}' is not in the models table.")

    try:
        result = provider.generate(req.prompt, model_name)
    except Exception as e:
        failed_request = LLMRequest(
            user_id=req.user_id, model_id=model_row.id, prompt=req.prompt,
            status="error", error=str(e),
        )
        db.add(failed_request)
        db.commit()
        raise HTTPException(502, f"LLM provider error: {e}")

    cost = calculate_cost(
        result.input_tokens, result.output_tokens,
        model_row.input_price_per_1m, model_row.output_price_per_1m,
    )

    saved_request = LLMRequest(
        user_id=req.user_id, model_id=model_row.id, prompt=req.prompt,
        input_tokens=result.input_tokens, output_tokens=result.output_tokens,
        latency_ms=result.latency_ms, cost=cost, status="success",
    )
    db.add(saved_request)
    db.flush()

    if routing_info:
        db.add(RoutingDecision(
            request_id=saved_request.id,
            complexity_score=routing_info.score,
            complexity_level=routing_info.level,
            selected_model=model_name,
            reason="; ".join(routing_info.reasons),
        ))

    db.commit()

    response_data = result.__dict__ | {"cost": float(cost)}
    if routing_info:
        response_data["complexity_score"] = routing_info.score
        response_data["complexity_level"] = routing_info.level
        response_data["routing_reason"] = "; ".join(routing_info.reasons)

    return ChatResponse(**response_data)