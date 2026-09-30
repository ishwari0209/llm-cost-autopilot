import re
from dataclasses import dataclass, field


@dataclass
class ComplexityResult:
    score: int
    level: str  # "LOW", "MEDIUM", "HIGH"
    reasons: list[str] = field(default_factory=list)


# Keywords that suggest harder reasoning or multi-step work
REASONING_KEYWORDS = [
    "analyze", "analyse", "compare", "evaluate", "explain why",
    "architecture", "design", "strategy", "optimi", "refactor",
    "debug", "root cause", "trade-off", "tradeoff",
]
CODING_KEYWORDS = [
    "code", "function", "bug", "error", "stack trace", "class ",
    "algorithm", "implement", "sql", "regex",
]
DOCUMENT_KEYWORDS = [
    "document", "report", "summarize", "summarise", "dataset",
    "pdf", "transcript", "logs",
]
MULTISTEP_KEYWORDS = [
    "step by step", "step-by-step", "then", "after that", "first,",
    "plan", "multi-step",
]


def score_prompt(prompt: str) -> ComplexityResult:
    text = prompt.lower()
    word_count = len(prompt.split())
    score = 0
    reasons: list[str] = []

    # --- Length / context size ---
    if word_count <= 15:
        score += 1
        reasons.append("short prompt (+1)")
    elif word_count <= 80:
        score += 2
        reasons.append("moderate length (+2)")
    else:
        score += 3
        reasons.append("large prompt / context (+3)")

    # --- Coding task ---
    if any(k in text for k in CODING_KEYWORDS) or "```" in prompt:
        score += 2
        reasons.append("coding task detected (+2)")

    # --- Multi-step reasoning ---
    if any(k in text for k in MULTISTEP_KEYWORDS):
        score += 3
        reasons.append("multi-step instructions detected (+3)")

    # --- Document / dataset analysis ---
    if any(k in text for k in DOCUMENT_KEYWORDS):
        score += 2
        reasons.append("document/data analysis detected (+2)")

    # --- General reasoning / analysis keywords ---
    if any(k in text for k in REASONING_KEYWORDS):
        score += 2
        reasons.append("reasoning/analysis keywords detected (+2)")

    # --- Multiple questions in one prompt ---
    question_count = len(re.findall(r"\?", prompt))
    if question_count >= 2:
        score += 1
        reasons.append(f"multiple questions detected (+1, {question_count} found)")

    # --- Map score to level ---
    if score <= 3:
        level = "LOW"
    elif score <= 6:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return ComplexityResult(score=score, level=level, reasons=reasons)