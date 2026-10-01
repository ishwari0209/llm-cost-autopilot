import { NavLink } from "react-router-dom";

const LINKS = [
  { to: "/", label: "Overview", icon: GridIcon, end: true },
  { to: "/requests", label: "Requests", icon: ListIcon },
  { to: "/routing", label: "Routing", icon: RouteIcon },
  { to: "/models", label: "Models", icon: StackIcon },
  { to: "/budget", label: "Budget", icon: GaugeIcon },
  { to: "/try-it", label: "Try it", icon: PlayIcon },
];

export default function Sidebar() {
  return (
    <aside className="w-56 shrink-0 border-r border-base-border bg-base-surface flex flex-col">
      <div className="px-4 py-4 border-b border-base-border">
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-tier-low" />
          <div className="h-2 w-2 rounded-full bg-tier-medium" />
          <div className="h-2 w-2 rounded-full bg-tier-high" />
        </div>
        <div className="mt-2 text-sm font-semibold tracking-tight text-base-text">
          Cost Autopilot
        </div>
        <div className="text-xs text-base-subtext">LLM routing gateway</div>
      </div>

      <nav className="flex-1 px-2 py-3 space-y-0.5">
        {LINKS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-2.5 px-2.5 py-2 rounded-sm text-sm transition-colors ${
                isActive
                  ? "bg-base-surface2 text-base-text"
                  : "text-base-subtext hover:text-base-text hover:bg-base-surface2/60"
              }`
            }
          >
            <Icon className="h-4 w-4 shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-4 py-3 border-t border-base-border text-xs text-base-muted">
        connected to API
      </div>
    </aside>
  );
}

function GridIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" {...props}>
      <rect x="3" y="3" width="8" height="8" rx="1.5" />
      <rect x="13" y="3" width="8" height="8" rx="1.5" />
      <rect x="3" y="13" width="8" height="8" rx="1.5" />
      <rect x="13" y="13" width="8" height="8" rx="1.5" />
    </svg>
  );
}
function ListIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" {...props}>
      <path d="M4 6h16M4 12h16M4 18h10" strokeLinecap="round" />
    </svg>
  );
}
function RouteIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" {...props}>
      <circle cx="6" cy="6" r="2.5" />
      <circle cx="18" cy="18" r="2.5" />
      <path d="M8.2 7.6C11 11 13 13 15.8 16.4" strokeLinecap="round" />
    </svg>
  );
}
function StackIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" {...props}>
      <path d="M12 3l9 4.5-9 4.5-9-4.5L12 3z" strokeLinejoin="round" />
      <path d="M3 12.5l9 4.5 9-4.5" strokeLinejoin="round" strokeLinecap="round" />
      <path d="M3 17l9 4.5 9-4.5" strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  );
}
function GaugeIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" {...props}>
      <path d="M4 15a8 8 0 1116 0" strokeLinecap="round" />
      <path d="M12 15l4-5" strokeLinecap="round" />
    </svg>
  );
}
function PlayIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" {...props}>
      <path d="M7 5l12 7-12 7V5z" strokeLinejoin="round" />
    </svg>
  );
}
