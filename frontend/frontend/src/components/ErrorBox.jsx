export default function ErrorBox({ message, onRetry }) {
  return (
    <div className="bg-tier-highBg border border-tier-high/30 rounded px-4 py-3 text-sm">
      <div className="text-tier-high font-medium mb-0.5">
        Couldn't load this data
      </div>
      <div className="text-base-subtext">{message}</div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 text-xs text-accent hover:underline"
        >
          Retry
        </button>
      )}
    </div>
  );
}
