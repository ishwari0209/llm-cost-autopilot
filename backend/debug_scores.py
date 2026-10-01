from app.router.complexity import score_prompt

prompts = [
    "Compare the trade-offs of serverless vs traditional server architecture for a growing e-commerce platform.",
    "Why do some countries maintain low inflation for decades while others experience chronic hyperinflation?",
    "Walk me through diagnosing a memory leak in a long-running Node.js service, prioritizing the most likely causes first.",
    "Evaluate whether a company should build its own ML infrastructure or rely on third-party APIs, considering cost and control.",
    "This SQL query is returning duplicate rows, what might be wrong?",
    "How many continents are there?",
]

for p in prompts:
    r = score_prompt(p)
    print(f"{r.score:3d}  {r.level:7s}  {p[:60]}")
    print(f"       reasons: {r.reasons}")