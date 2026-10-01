import { useApi } from "../useApi.js";
import { api } from "../api.js";

const TIER_STYLES = {
  normal: "text-tier-low bg-tier-lowBg border-tier-low/30",
  warning: "text-tier-medium bg-tier-mediumBg border-tier-medium/30",
  restricted: "text-tier-high bg-tier-highBg border-tier-high/30",
  blocked: "text-base-bg bg-tier-high border-tier-high",
};

export default function TopBar({ title }) {
  const { data } = useApi(() => api.budget(), [], { pollMs: 10000 });

  return (
    <header className="h-14 shrink-0 border-b border-base-border bg-base-bg flex items-center justify-between px-6">
      <h1 className="text-sm font-medium text-base-text">{title}</h1>

      {data && (
        <div
          className={`flex items-center gap-2 px-2.5 py-1 rounded-sm border text-xs font-mono ${
            TIER_STYLES[data.tier] || ""
          }`}
          title={`$${data.spent.toFixed(2)} of $${data.limit.toFixed(2)} spent this month`}
        >
          <span className="h-1.5 w-1.5 rounded-full bg-current" />
          budget: {data.tier} · {data.percent_used.toFixed(0)}%
        </div>
      )}
    </header>
  );
}
