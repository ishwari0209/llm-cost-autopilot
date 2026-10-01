from app.core.config import settings

LEVEL_TO_MODEL = {
    "LOW": "gemini-3.5-flash-lite",
    "MEDIUM": "gemini-3.6-flash",
    "HIGH": "gemini-3.6-flash",
}


def select_model(level: str) -> str:
    return LEVEL_TO_MODEL.get(level, settings.default_model)