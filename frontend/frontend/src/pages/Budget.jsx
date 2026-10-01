import { useState, useEffect } from "react";
import { api } from "../api.js";
import { useApi } from "../useApi.js";
import Card from "../components/Card.jsx";
import Loading from "../components/Loading.jsx";
import ErrorBox from "../components/ErrorBox.jsx";

const TIER_LABEL = {
  normal: "Normal — routing as usual",
  warning: "Warning — approaching the limit",
  restricted: "Restricted — forcing the cheapest model",
  blocked: "Blocked — requests are rejected",
};

const TIER_BAR_COLOR = {
  normal: "bg-tier-low",
  warning: "bg-tier-medium",
  restricted: "bg-tier-high",
  blocked: "bg-tier-high",
};

export default function Budget() {
  const { data, error, loading, refetch } = useApi(() => api.budget(), []);

  return (
    <div className="space-y-4">
      <Card title="Current spend" subtitle="This calendar month">
        {loading ? (
          <Loading />
        ) : error ? (
          <ErrorBox message={error} onRetry={refetch} />
        ) : (
          <SpendView data={data} />
        )}
      </Card>

      {data && !loading && !error && (
        <EditPanel data={data} onSaved={refetch} />
      )}
    </div>
  );
}

function SpendView({ data }) {
  const pct = Math.min(100, data.percent_used);
  return (
    <div>
      <div className="flex items-end justify-between mb-2">
        <div className="font-mono text-2xl text-base-text">
          ${data.spent.toFixed(4)}
          <span className="text-base-subtext text-base font-normal">
            {" "}
            / ${data.limit.toFixed(2)}
          </span>
        </div>
        <div className="font-mono text-sm text-base-subtext">
          {data.percent_used.toFixed(1)}%
        </div>
      </div>

      <div className="h-2.5 w-full bg-base-surface2 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${TIER_BAR_COLOR[data.tier]}`}
          style={{ width: `${pct}%` }}
        />
      </div>

      <div className="flex items-center justify-between mt-1.5 text-xs text-base-muted">
        <span>$0</span>
        <span>warning {data.warning_threshold}%</span>
        <span>restricted {data.restricted_threshold}%</span>
        <span>100%</span>
      </div>

      <p className="mt-4 text-sm text-base-text">{TIER_LABEL[data.tier]}</p>
    </div>
  );
}

function EditPanel({ data, onSaved }) {
  const [limit, setLimit] = useState(data.limit);
  const [warning, setWarning] = useState(data.warning_threshold);
  const [restricted, setRestricted] = useState(data.restricted_threshold);
  const [saving, setSaving] = useState(null);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    setLimit(data.limit);
    setWarning(data.warning_threshold);
    setRestricted(data.restricted_threshold);
  }, [data]);

  async function save(field) {
    setSaving(field);
    setMessage(null);
    try {
      if (field === "limit") await api.setBudgetLimit(Number(limit));
      if (field === "warning") await api.setWarningThreshold(Number(warning));
      if (field === "restricted")
        await api.setRestrictedThreshold(Number(restricted));
      setMessage({ field, text: "Saved" });
      onSaved();
    } catch (err) {
      setMessage({ field, text: err.message, error: true });
    } finally {
      setSaving(null);
    }
  }

  return (
    <Card title="Policy" subtitle="Changes take effect immediately, no restart needed">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Field
          label="Monthly limit ($)"
          value={limit}
          onChange={setLimit}
          onSave={() => save("limit")}
          saving={saving === "limit"}
          message={message?.field === "limit" ? message : null}
          step="0.01"
        />
        <Field
          label="Warning threshold (%)"
          value={warning}
          onChange={setWarning}
          onSave={() => save("warning")}
          saving={saving === "warning"}
          message={message?.field === "warning" ? message : null}
          step="1"
        />
        <Field
          label="Restricted threshold (%)"
          value={restricted}
          onChange={setRestricted}
          onSave={() => save("restricted")}
          saving={saving === "restricted"}
          message={message?.field === "restricted" ? message : null}
          step="1"
        />
      </div>
    </Card>
  );
}

function Field({ label, value, onChange, onSave, saving, message, step }) {
  return (
    <div>
      <label className="block text-xs text-base-subtext mb-1.5">{label}</label>
      <div className="flex gap-2">
        <input
          type="number"
          step={step}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full bg-base-surface2 border border-base-border rounded-sm px-2.5 py-1.5 text-sm font-mono text-base-text focus:border-accent outline-none"
        />
        <button
          onClick={onSave}
          disabled={saving}
          className="px-3 py-1.5 text-xs font-medium bg-accent/15 text-accent border border-accent/30 rounded-sm hover:bg-accent/25 disabled:opacity-50 transition-colors whitespace-nowrap"
        >
          {saving ? "Saving…" : "Save"}
        </button>
      </div>
      {message && (
        <p
          className={`mt-1 text-xs ${
            message.error ? "text-tier-high" : "text-tier-low"
          }`}
        >
          {message.text}
        </p>
      )}
    </div>
  );
}
