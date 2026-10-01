import { api } from "../api.js";
import { useApi } from "../useApi.js";
import Card from "../components/Card.jsx";
import Loading from "../components/Loading.jsx";
import ErrorBox from "../components/ErrorBox.jsx";
import StatusBadge from "../components/StatusBadge.jsx";

export default function Requests() {
  const { data, error, loading, refetch } = useApi(() => api.requests(50), []);

  return (
    <Card title="Recent requests" subtitle="Last 50, newest first">
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorBox message={error} onRetry={refetch} />
      ) : data.length === 0 ? (
        <div className="text-sm text-base-subtext text-center py-10">
          No requests logged yet.
        </div>
      ) : (
        <div className="overflow-x-auto -mx-4">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-base-subtext border-b border-base-border">
                <th className="px-4 py-2 font-medium">Time</th>
                <th className="px-4 py-2 font-medium">Model</th>
                <th className="px-4 py-2 font-medium text-right">In tok</th>
                <th className="px-4 py-2 font-medium text-right">Out tok</th>
                <th className="px-4 py-2 font-medium text-right">Cost</th>
                <th className="px-4 py-2 font-medium text-right">Latency</th>
                <th className="px-4 py-2 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="font-mono text-xs">
              {data.map((r) => (
                <tr
                  key={r.id}
                  className="border-b border-base-border/60 last:border-0"
                >
                  <td className="px-4 py-2 text-base-subtext whitespace-nowrap">
                    {new Date(r.created_at).toLocaleString()}
                  </td>
                  <td className="px-4 py-2 text-base-text">{r.model}</td>
                  <td className="px-4 py-2 text-right text-base-subtext">
                    {r.input_tokens}
                  </td>
                  <td className="px-4 py-2 text-right text-base-subtext">
                    {r.output_tokens}
                  </td>
                  <td className="px-4 py-2 text-right text-base-text">
                    ${r.cost.toFixed(5)}
                  </td>
                  <td className="px-4 py-2 text-right text-base-subtext">
                    {Math.round(r.latency_ms)} ms
                  </td>
                  <td className="px-4 py-2">
                    <StatusBadge status={r.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
}
