import json
import time
from pathlib import Path

import requests

API_URL = "http://127.0.0.1:8000/v1/chat"

PROMPTS_FILE = Path(__file__).parent / "final_holdout.json"
RESULTS_FILE = Path(__file__).parent / "final_holdout_results.json"

DELAY_BETWEEN_CALLS = 4  # seconds
MAX_RETRIES = 3


def call(prompt: str, model: str | None = None, router_type: str = "rules"):
    body = {"prompt": prompt, "user_id": 1, "router_type": router_type}
    if model:
        body["model"] = model

    for attempt in range(MAX_RETRIES):
        resp = requests.post(API_URL, json=body, timeout=120)
        if resp.status_code == 200:
            return resp.json()

        # Rate limit or overload — wait longer and retry
        if resp.status_code in (429, 502):
            wait = 15 * (attempt + 1)
            print(f"    got {resp.status_code}, retrying in {wait}s...")
            time.sleep(wait)
            continue

        return {"error": resp.text}

    return {"error": f"failed after {MAX_RETRIES} retries"}


def main():
    prompts = json.loads(PROMPTS_FILE.read_text())
    results = []

    for item in prompts:
        print(f"[{item['id']}] {item['prompt'][:60]}...")

        rules_result = call(item["prompt"], router_type="rules")
        time.sleep(DELAY_BETWEEN_CALLS)
        llm_result = call(item["prompt"], router_type="llm")
        time.sleep(DELAY_BETWEEN_CALLS)

        results.append({
            "id": item["id"],
            "prompt": item["prompt"],
            "expected": item["expected"],
            "rules": rules_result,
            "llm": llm_result,
        })

    RESULTS_FILE.write_text(json.dumps(results, indent=2))
    print(f"\nSaved {len(results)} results to {RESULTS_FILE}")


if __name__ == "__main__":
    main()