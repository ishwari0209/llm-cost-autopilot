import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
} from "recharts";
import { api } from "../api.js";
import { useApi } from "../useApi.js";
import Card from "../components/Card.jsx";
import StatTile from "../components/StatTile.jsx";
import Loading from "../components/Loading.jsx";
import ErrorBox from "../components/ErrorBox.jsx";

const MODEL_COLORS = {
  "gemini-3.5-flash-lite": "#5A9B7C",
  "gemini-3.6-flash": "#C9A227",
  "gemini-3.1-pro-preview": "#C06B57",
};

function fmtUsd(n) {
  return `$${Number(n ?? 0).toFixed(4)}`;
}

function fmtNum(n) {
  return new Intl.NumberFormat("en-US").format(n ?? 0);
}

export default function Overview() {
  const summary = useApi(() => api.summary(), []);
  const costOverTime = useApi(() => api.costOverTime(14), []);
  const modelUsage = useApi(() => api.modelUsage(), []);
  const today = useApi(() => api.usageToday(), [], { pollMs: 10000 });

  return (
    <div className="space-y-6">
      {summary.loading ? (
        <Loading label="Loading summary…" />
      ) : summary.error ? (
        <ErrorBox message={summary.error} onRetry={summary.refetch} />
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <StatTile
            label="Total requests"
            value={fmtNum(summary.data.total_requests)}
          />
          <StatTile
            label="Total tokens"
            value={fmtNum(summary.data.total_tokens)}
          />
          <StatTile
            label="Total cost"
            value={fmtUsd(summary.data.total_cost)}
          />
          <StatTile
            label="Avg latency"
            value={`${Math.round(summary.data.avg_latency_ms)} ms`}
          />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card title="Cost over time" subtitle="Last 14 days" className="lg:col-span-2">
          {costOverTime.loading ? (
            <Loading />
          ) : costOverTime.error ? (
            <ErrorBox message={costOverTime.error} onRetry={costOverTime.refetch} />
          ) : costOverTime.data.length === 0 ? (
            <EmptyState text="No requests logged yet. Send a prompt from Try it to see cost data here." />
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={costOverTime.data}>
                <CartesianGrid stroke="#2A313C" vertical={false} />
                <XAxis
                  dataKey="date"
                  stroke="#5B6472"
                  fontSize={11}
                  tickLine={false}
                  axisLine={{ stroke: "#2A313C" }}
                />
                <YAxis
                  stroke="#5B6472"
                  fontSize={11}
                  tickLine={false}
                  axisLine={{ stroke: "#2A313C" }}
                  tickFormatter={(v) => `$${v}`}
                  width={56}
                />
                <Tooltip
                  contentStyle={{
                    background: "#161B22",
                    border: "1px solid #2A313C",
                    borderRadius: 6,
                    fontSize: 12,
                  }}
                  labelStyle={{ color: "#8B95A1" }}
                  formatter={(v) => [fmtUsd(v), "cost"]}
                />
                <Line
                  type="monotone"
                  dataKey="cost"
                  stroke="#4E8CD9"
                  strokeWidth={2}
                  dot={{ r: 2.5, fill: "#4E8CD9" }}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </Card>

        <Card title="Today" subtitle="Live, updates every 10s">
          {today.loading ? (
            <Loading />
          ) : today.error ? (
            <ErrorBox message={today.error} onRetry={today.refetch} />
          ) : (
            <div className="space-y-3">
              <Row label="Requests" value={fmtNum(today.data.requests_today)} />
              <Row label="Tokens" value={fmtNum(today.data.tokens_today)} />
              <Row label="Cost" value={fmtUsd(today.data.cost_today)} />
            </div>
          )}
        </Card>
      </div>

      <Card title="Model usage" subtitle="Share of requests per model">
        {modelUsage.loading ? (
          <Loading />
        ) : modelUsage.error ? (
          <ErrorBox message={modelUsage.error} onRetry={modelUsage.refetch} />
        ) : modelUsage.data.length === 0 ? (
          <EmptyState text="No requests yet." />
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={modelUsage.data} layout="vertical" margin={{ left: 8 }}>
              <CartesianGrid stroke="#2A313C" horizontal={false} />
              <XAxis
                type="number"
                stroke="#5B6472"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: "#2A313C" }}
              />
              <YAxis
                type="category"
                dataKey="model"
                stroke="#8B95A1"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                width={160}
              />
              <Tooltip
                contentStyle={{
                  background: "#161B22",
                  border: "1px solid #2A313C",
                  borderRadius: 6,
                  fontSize: 12,
                }}
                formatter={(v) => [fmtNum(v), "requests"]}
              />
              <Bar dataKey="count" radius={[0, 3, 3, 0]}>
                {modelUsage.data.map((d) => (
                  <Cell key={d.model} fill={MODEL_COLORS[d.model] || "#4E8CD9"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </Card>
    </div>
  );
}

function Row({ label, value }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-base-subtext">{label}</span>
      <span className="font-mono text-sm text-base-text">{value}</span>
    </div>
  );
}

function EmptyState({ text }) {
  return (
    <div className="text-sm text-base-subtext text-center py-10">{text}</div>
  );
}
