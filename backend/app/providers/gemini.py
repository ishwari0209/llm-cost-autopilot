import time
from dataclasses import dataclass

from google import genai

from app.core.config import settings


@dataclass
class LLMResult:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float


class GeminiProvider:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate(self, prompt: str, model: str) -> LLMResult:
        start = time.perf_counter()
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )
        latency_ms = (time.perf_counter() - start) * 1000

        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count or 0
        # Some Gemini models "think" before answering. Those tokens are billed
        # as output, so we count them too.
        output_tokens = (usage.candidates_token_count or 0) + (
            usage.thoughts_token_count or 0
        )

        return LLMResult(
            text=response.text or "",
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=round(latency_ms, 1),
        )