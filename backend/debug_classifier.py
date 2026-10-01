# backend/debug_classifier.py
from app.router.llm_classifier import classify_prompt

result = classify_prompt("Why do people get more anxious the night before a big event?")
print(result)