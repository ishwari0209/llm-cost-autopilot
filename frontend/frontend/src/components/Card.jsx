export default function Card({ title, subtitle, children, className = "" }) {
  return (
    <div
      className={`bg-base-surface border border-base-border rounded ${className}`}
    >
      {(title || subtitle) && (
        <div className="px-4 py-3 border-b border-base-border">
          {title && (
            <h3 className="text-sm font-medium text-base-text">{title}</h3>
          )}
          {subtitle && (
            <p className="text-xs text-base-subtext mt-0.5">{subtitle}</p>
          )}
        </div>
      )}
      <div className="p-4">{children}</div>
    </div>
  );
}
