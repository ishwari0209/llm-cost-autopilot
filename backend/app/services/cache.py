import hashlib
import json

from app.core.redis_client import redis_client

CACHE_TTL_SECONDS = 3600


def cache_key(prompt: str, model: str) -> str:
    raw = f"{model}:{prompt}"
    return "cache:" + hashlib.sha256(raw.encode()).hexdigest()


def get_cached_response(prompt: str, model: str) -> dict | None:
    key = cache_key(prompt, model)
    cached = redis_client.get(key)
    return json.loads(cached) if cached else None


def set_cached_response(prompt: str, model: str, response: dict):
    key = cache_key(prompt, model)
    redis_client.setex(key, CACHE_TTL_SECONDS, json.dumps(response))