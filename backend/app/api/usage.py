
from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.db.models import User
from app.services.usage import get_today_usage

router = APIRouter(prefix="/v1", tags=["usage"])


@router.get("/usage/today")
def usage_today(
    current_user: User = Depends(get_current_user),
):
    return get_today_usage(current_user.id)