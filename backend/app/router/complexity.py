import re
from dataclasses import dataclass, field


@dataclass
class ComplexityResult:
    score: int
    level: str  # LOW, MEDIUM, HIGH
    reasons: list[str] = field(default_factory=list)


# Signals that suggest deep reasoning, synthesis, or open-ended judgment
HIGH_KEYWORDS = [
    "analyze", "analyse", "compare", "evaluate", "design",
    "architecture", "root cause", "propose", "trade-off", "tradeoff",
    "strategy", "optimize", "optimise", "refactor",
    "diagnos", "troubleshoot", "investigate",
]
# Causal "why" questions tend to need real reasoning, not just a fact lookup
CAUSAL_PATTERNS = [
    r"\bwhy do\b", r"\bwhy does\b", r"\bwhy did\b", r"\bwhy is it that\b",
]

# Signals of a moderately involved task: coding help, comparisons,
# advice-seeking, or general explanation
MEDIUM_KEYWORDS = [
    "how do i", "how should i", "how can i", "should i", "should a",
    "difference between", "explain", "debug", "function", "code",
    "stack trace", "best way to", "what causes",
    "duplicate", "not working", "unexpected", "returning wrong",
]

MULTISTEP_KEYWORDS = [
    "step by step", "step-by-step", "then", "after that", "first,",
    "plan", "multi-step", "walk me through",
]

# General patterns for short factual lookups — structural, not content-specific
SIMPLE_PATTERNS = [
    r"^what is the capital",
    r"^what is an? \w+\??$",          # "What is an API?", "What is a cell?"
    r"^define .+ in one sentence",
    r"^what year did",
    r"^give me a synonym",
    r"^translate ",
    r"^what('s| is) \d+",             # "What is 15% of 240?"
    r"^list \d+",
    r"^summarize .+ in \d+ sentences",
]


def score_prompt(prompt: str) -> ComplexityResult:
    text = prompt.lower().strip()
    score = 0
    reasons: list[str] = []

    # --- Fast path: clearly simple factual lookups ---
    if any(re.search(pattern, text) for pattern in SIMPLE_PATTERNS):
        return ComplexityResult(score=0, level="LOW", reasons=["simple factual request"])

    # --- Length / context size ---
    word_count = len(prompt.split())
    if word_count > 60:
        score += 2
        reasons.append("large context (+2)")
    elif word_count > 30:
        score += 1
        reasons.append("moderate context (+1)")

    # --- High-complexity keywords ---
    high_matches = [k for k in HIGH_KEYWORDS if k in text]
    if high_matches:
        score += 4
        reasons.append(f"high-complexity reasoning keywords: {', '.join(high_matches[:3])} (+4)")

    # --- Causal "why" reasoning ---
    causal_matches = [p for p in CAUSAL_PATTERNS if re.search(p, text)]
    if causal_matches:
        score += 4
        reasons.append("causal reasoning question (+4)")

    # --- Multi-step instructions ---
    if any(k in text for k in MULTISTEP_KEYWORDS):
        score += 3
        reasons.append("multi-step task (+3)")

    # --- Medium-complexity keywords (only count if HIGH didn't already fire) ---
    medium_matches = [k for k in MEDIUM_KEYWORDS if k in text]
    if medium_matches and not high_matches and not causal_matches:
        score += 2
        reasons.append(f"moderate reasoning keywords: {', '.join(medium_matches[:3])} (+2)")

    # --- Multiple questions bundled together ---
    if len(re.findall(r"\?", prompt)) >= 2:
        score += 1
        reasons.append("multiple questions (+1)")

    # --- Final classification ---
    if score >= 4:
        level = "HIGH"
    elif score >= 2:
        level = "MEDIUM"
    else:
        level = "LOW"

    return ComplexityResult(score=score, level=level, reasons=reasons)