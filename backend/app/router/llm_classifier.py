import json

from google import genai

from app.core.config import settings
from app.router.complexity import ComplexityResult

# Use the cheapest, fastest model for classification — this call happens
# on every "auto" request, so cost and latency here matter a lot.
CLASSIFIER_MODEL = "gemini-3.5-flash-lite"

client = genai.Client(api_key=settings.gemini_api_key)

CLASSIFIER_PROMPT_TEMPLATE = """You are a request complexity classifier for an \
LLM routing system. Classify the complexity of answering the user's question \
well, not how long the question is.

LOW: simple factual lookups, definitions, translations, basic arithmetic, \
short conversions. A correct answer is short and doesn't require judgment.

MEDIUM: questions needing some explanation, comparison, troubleshooting, or \
personal advice, but answerable without deep multi-step reasoning.

HIGH: questions needing real analysis, synthesis across multiple factors, \
system design, root-cause investigation, or open-ended judgment calls with \
trade-offs.

Question: {prompt}

Reply with strict JSON only, no markdown, in this exact format:
{{"level": "LOW" or "MEDIUM" or "HIGH", "reason": "one short sentence"}}"""


def classify_prompt(prompt: str) -> ComplexityResult:
    classifier_prompt = CLASSIFIER_PROMPT_TEMPLATE.format(prompt=prompt)

    try:
        response = client.models.generate_content(
            model=CLASSIFIER_MODEL,
            contents=classifier_prompt,
        )
        text = (response.text or "").strip()
        text = text.removeprefix("```json").removesuffix("```").strip()
        parsed = json.loads(text)

        level = parsed.get("level", "MEDIUM").upper()
        if level not in ("LOW", "MEDIUM", "HIGH"):
            level = "MEDIUM"
        reason = parsed.get("reason", "llm classifier decision")

        return ComplexityResult(score=-1, level=level, reasons=[reason])

    except Exception as e:
        # If the classifier call fails or returns bad JSON, fail safe to
        # MEDIUM rather than crashing the whole request.
        return ComplexityResult(
            score=-1,
            level="MEDIUM",
            reasons=[f"llm classifier failed, defaulted to MEDIUM: {e}"],
        )