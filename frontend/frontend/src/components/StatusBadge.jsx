export default function StatusBadge({ status }) {
  const ok = status === "success";
  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs font-medium ${
        ok ? "text-tier-low" : "text-tier-high"
      }`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${
          ok ? "bg-tier-low" : "bg-tier-high"
        }`}
      />
      {ok ? "success" : "error"}
    </span>
  );
}
