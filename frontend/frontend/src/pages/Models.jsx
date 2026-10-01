import { api } from "../api.js";
import { useApi } from "../useApi.js";
import Card from "../components/Card.jsx";
import Loading from "../components/Loading.jsx";
import ErrorBox from "../components/ErrorBox.jsx";

export default function Models() {
  const { data, error, loading, refetch } = useApi(() => api.models(), []);

  return (
    <Card title="Configured models" subtitle="Pricing per 1M tokens, from the database">
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorBox message={error} onRetry={refetch} />
      ) : data.length === 0 ? (
        <div className="text-sm text-base-subtext text-center py-10">
          No models configured. Run seed.py on the backend.
        </div>
      ) : (
        <div className="overflow-x-auto -mx-4">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-base-subtext border-b border-base-border">
                <th className="px-4 py-2 font-medium">Provider</th>
                <th className="px-4 py-2 font-medium">Model</th>
                <th className="px-4 py-2 font-medium text-right">Input $/1M</th>
                <th className="px-4 py-2 font-medium text-right">Output $/1M</th>
              </tr>
            </thead>
            <tbody className="font-mono text-xs">
              {data.map((m) => (
                <tr
                  key={m.id}
                  className="border-b border-base-border/60 last:border-0"
                >
                  <td className="px-4 py-2.5 text-base-subtext">{m.provider}</td>
                  <td className="px-4 py-2.5 text-base-text">{m.model_name}</td>
                  <td className="px-4 py-2.5 text-right text-base-text">
                    ${m.input_price_per_1m.toFixed(2)}
                  </td>
                  <td className="px-4 py-2.5 text-right text-base-text">
                    ${m.output_price_per_1m.toFixed(2)}
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
