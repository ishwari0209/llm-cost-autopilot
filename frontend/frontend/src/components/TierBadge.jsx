const STYLES = {
  LOW: "text-tier-low bg-tier-lowBg border-tier-low/30",
  MEDIUM: "text-tier-medium bg-tier-mediumBg border-tier-medium/30",
  HIGH: "text-tier-high bg-tier-highBg border-tier-high/30",
};

export default function TierBadge({ level }) {
  const style = STYLES[level] || "text-base-subtext bg-base-surface2 border-base-border";
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-sm border text-xs font-medium font-mono ${style}`}
    >
      {level || "—"}
    </span>
  );
}
