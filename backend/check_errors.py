# add to check_errors.py, or a new script
import json
from pathlib import Path

results = json.loads((Path("eval") / "final_holdout_results.json").read_text())

rules_latencies = [r["rules"]["latency_ms"] for r in results if "error" not in r["rules"]]
llm_latencies = [r["llm"]["latency_ms"] for r in results if "error" not in r["llm"]]

print(f"Rules-based avg latency: {sum(rules_latencies)/len(rules_latencies):.0f} ms")
print(f"LLM-classifier avg latency: {sum(llm_latencies)/len(llm_latencies):.0f} ms")