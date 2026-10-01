from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.db import models  # noqa: F401  (registers the tables)
from app.db.session import Base, engine
from app.api.usage import router as usage_router
from app.api.budget import router as budget_router
from app.api.stats import router as stats_router
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Cost Autopilot")
app.include_router(chat_router)
app.include_router(usage_router)
app.include_router(budget_router)
app.include_router(stats_router)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    return {"status": "ok"}