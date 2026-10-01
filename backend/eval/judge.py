import json
from pathlib import Path

from google import genai
from google.genai.errors import ClientError

from app.core.config import settings

RESULTS_FILE = Path(__file__).parent / "results.json"
JUDGED_FILE = Path(__file__).parent / "judged.json"

JUDGE_MODEL = "gemini-3.6-flash"

client = genai.Client(api_key=settings.gemini_api_key)


def judge_answer(prompt: str, answer: str) -> dict:
    judge_prompt = f"""You are grading whether an AI answer is acceptable.

Question: {prompt}

Answer: {answer}

Is this answer acceptable (correct, complete enough, and clear) for the
question asked? Reply with strict JSON only, no markdown, in this exact
format:
{{"acceptable": true or false, "reason": "one short sentence"}}"""

    try:
        response = client.models.generate_content(
            model=JUDGE_MODEL,
            contents=judge_prompt,
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "acceptable": None,
                "reason": f"could not parse judge output: {text[:100]}"
            }

    except ClientError as e:
        if e.code == 429:
            return {
                "acceptable": None,
                "reason": "Gemini API quota exceeded"
            }

        return {
            "acceptable": None,
            "reason": f"Gemini API error: {e}"
        }


def main():
    results = json.loads(RESULTS_FILE.read_text())

    for item in results:
        for tier in ("cheap", "strong"):
            resp = item[tier]

            if "error" in resp:
                item[tier]["judged"] = {
                    "acceptable": None,
                    "reason": "request failed"
                }
                continue

            # Skip already judged answers
            if "judged" in item[tier]:
                print(f"[{item['id']}] {tier} already judged, skipping...")
                continue

            print(f"[{item['id']}] judging {tier}...")

            judged = judge_answer(
                item["prompt"],
                resp["text"]
            )

            item[tier]["judged"] = judged

            # Save immediately after each judgment
            JUDGED_FILE.write_text(
                json.dumps(results, indent=2)
            )

            # Stop if quota is exhausted
            if (
                judged["acceptable"] is None
                and judged["reason"] == "Gemini API quota exceeded"
            ):
                print("\nGemini quota exceeded.")
                print(f"Partial results saved to {JUDGED_FILE}")
                return

    print(f"\nSaved judged results to {JUDGED_FILE}")


if __name__ == "__main__":
    main()