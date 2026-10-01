import { api } from "../api.js";
import { useApi } from "../useApi.js";
import Card from "../components/Card.jsx";
import Loading from "../components/Loading.jsx";
import ErrorBox from "../components/ErrorBox.jsx";
import TierBadge from "../components/TierBadge.jsx";

export default function Routing() {
  const { data, error, loading, refetch } = useApi(
    () => api.routingDecisions(50),
    []
  );

  return (
    <Card title="Routing decisions" subtitle="Why each request went where it did">
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorBox message={error} onRetry={refetch} />
      ) : data.length === 0 ? (
        <div className="text-sm text-base-subtext text-center py-10">
          No routing decisions logged yet.
        </div>
      ) : (
        <div className="divide-y divide-base-border">
          {data.map((d) => (
            <div key={d.id} className="py-3 first:pt-0 last:pb-0">
              <div className="flex items-start justify-between gap-4">
                <p className="text-sm text-base-text flex-1">{d.prompt}</p>
                <div className="flex items-center gap-2 shrink-0">
                  <span className="font-mono text-xs text-base-subtext">
                    score {d.complexity_score}
                  </span>
                  <TierBadge level={d.complexity_level} />
                </div>
              </div>
              <div className="mt-1.5 flex items-center gap-2 text-xs">
                <span className="font-mono text-accent">{d.selected_model}</span>
                <span className="text-base-muted">·</span>
                <span className="text-base-subtext">{d.reason}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
