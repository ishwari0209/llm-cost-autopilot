export default function StatTile({ label, value, sub }) {
  return (
    <div className="bg-base-surface border border-base-border rounded px-4 py-3.5">
      <div className="text-xs text-base-subtext mb-1.5">{label}</div>
      <div className="font-mono text-2xl text-base-text leading-none">
        {value}
      </div>
      {sub && <div className="text-xs text-base-muted mt-1.5">{sub}</div>}
    </div>
  );
}
