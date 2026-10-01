import json
from pathlib import Path

RESULTS_FILE = Path(__file__).parent / "final_holdout_results.json"


def main():
    results = json.loads(RESULTS_FILE.read_text())
    total = len(results)

    rules_correct = rules_errors = 0
    llm_correct = llm_errors = 0
    rules_cost = llm_cost = 0.0

    for item in results:
        expected = item["expected"]

        if "error" in item["rules"]:
            rules_errors += 1
        elif item["rules"].get("complexity_level") == expected:
            rules_correct += 1
        rules_cost += item["rules"].get("cost", 0)

        if "error" in item["llm"]:
            llm_errors += 1
        elif item["llm"].get("complexity_level") == expected:
            llm_correct += 1
        llm_cost += item["llm"].get("cost", 0)

    rules_valid = total - rules_errors
    llm_valid = total - llm_errors

    print(f"Rules-based: {rules_correct}/{rules_valid} valid calls correct ({rules_errors} errored)")
    print(f"LLM-classifier: {llm_correct}/{llm_valid} valid calls correct ({llm_errors} errored)")
    print(f"Rules-based cost: ${rules_cost:.6f}")
    print(f"LLM-classifier cost: ${llm_cost:.6f}")


if __name__ == "__main__":
    main()