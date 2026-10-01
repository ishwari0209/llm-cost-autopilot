import { useState } from "react";
import { api } from "../api.js";
import Card from "../components/Card.jsx";
import TierBadge from "../components/TierBadge.jsx";
import ErrorBox from "../components/ErrorBox.jsx";

export default function TryIt() {
  const [prompt, setPrompt] = useState("");
  const [routerType, setRouterType] = useState("llm");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function send() {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await api.chat({
        prompt: prompt.trim(),
        router_type: routerType,
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <Card title="Send a prompt" subtitle="Routed live through the gateway">
        <div className="space-y-3">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask anything — a quick fact, a coding question, or something that needs real analysis…"
            rows={4}
            className="w-full bg-base-surface2 border border-base-border rounded-sm px-3 py-2.5 text-sm text-base-text placeholder:text-base-muted focus:border-accent outline-none resize-none"
          />
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <label className="text-xs text-base-subtext">Router</label>
              <select
                value={routerType}
                onChange={(e) => setRouterType(e.target.value)}
                className="bg-base-surface2 border border-base-border rounded-sm px-2 py-1.5 text-xs font-mono text-base-text focus:border-accent outline-none"
              >
                <option value="llm">llm classifier</option>
                <option value="rules">rule-based</option>
              </select>
            </div>
            <button
              onClick={send}
              disabled={loading || !prompt.trim()}
              className="px-4 py-1.5 text-sm font-medium bg-accent/15 text-accent border border-accent/30 rounded-sm hover:bg-accent/25 disabled:opacity-40 transition-colors"
            >
              {loading ? "Routing…" : "Send"}
            </button>
          </div>
        </div>
      </Card>

      {error && <ErrorBox message={error} />}

      {result && <ResultView result={result} />}
    </div>
  );
}

function ResultView({ result }) {
  return (
    <Card title="Response">
      <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          <TierBadge level={result.complexity_level} />
          <span className="font-mono text-xs text-accent">{result.model}</span>
          {result.fallback && (
            <span className="font-mono text-xs text-tier-medium bg-tier-mediumBg border border-tier-medium/30 rounded-sm px-2 py-0.5">
              fallback: {result.fallback_reason}
            </span>
          )}
        </div>

        {result.routing_reason && (
          <p className="text-xs text-base-subtext italic">
            "{result.routing_reason}"
          </p>
        )}

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <Metric label="Cost" value={`$${result.cost.toFixed(5)}`} />
          <Metric label="Latency" value={`${Math.round(result.latency_ms)} ms`} />
          <Metric label="Input tok" value={result.input_tokens} />
          <Metric label="Output tok" value={result.output_tokens} />
        </div>

        <div className="pt-2 border-t border-base-border">
          <p className="text-sm text-base-text whitespace-pre-wrap leading-relaxed">
            {result.text}
          </p>
        </div>
      </div>
    </Card>
  );
}

function Metric({ label, value }) {
  return (
    <div className="bg-base-surface2 rounded-sm px-2.5 py-2">
      <div className="text-[11px] text-base-subtext">{label}</div>
      <div className="font-mono text-sm text-base-text mt-0.5">{value}</div>
    </div>
  );
}
