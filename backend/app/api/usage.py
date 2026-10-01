from fastapi import APIRouter

from app.services.usage import get_today_usage

router = APIRouter(prefix="/v1", tags=["usage"])


@router.get("/usage/today")
def usage_today():
    return get_today_usage()