export default function Loading({ label = "Loading…" }) {
  return (
    <div className="flex items-center gap-2 text-sm text-base-subtext py-6 justify-center">
      <span className="h-3.5 w-3.5 border-2 border-base-border border-t-accent rounded-full animate-spin" />
      {label}
    </div>
  );
}
