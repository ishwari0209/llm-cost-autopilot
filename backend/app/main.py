from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.db import models  # noqa: F401  (registers the tables)
from app.db.session import Base, engine
from app.api.usage import router as usage_router
...

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Cost Autopilot")
app.include_router(chat_router)
app.include_router(usage_router)

@app.get("/health")
def health():
    return {"status": "ok"}