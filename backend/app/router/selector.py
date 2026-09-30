from app.core.config import settings

# LOW and MEDIUM share a model for now since you only have 2 working tiers.
# Add a third entry here once your strong model (e.g. the pro model) works.
LEVEL_TO_MODEL = {
    "LOW": "gemini-3.5-flash-lite",
    "MEDIUM": "gemini-3.5-flash-lite",
    "HIGH": "gemini-3.6-flash",
}


def select_model(level: str) -> str:
    return LEVEL_TO_MODEL.get(level, settings.default_model)