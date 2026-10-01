
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar.jsx";
import TopBar from "./components/TopBar.jsx";
import Overview from "./pages/Overview.jsx";
import RequestsPage from "./pages/Requests.jsx";
import Routing from "./pages/Routing.jsx";
import Models from "./pages/Models.jsx";
import Budget from "./pages/Budget.jsx";
import TryIt from "./pages/TryIt.jsx";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";
import { authStorage } from "./api";

const TITLES = {
  "/": "Overview",
  "/requests": "Requests",
  "/routing": "Routing decisions",
  "/models": "Models",
  "/budget": "Budget",
  "/try-it": "Try it",
};

function ProtectedDashboard() {
  const location = useLocation();
  const user = authStorage.getUser();
  const token = authStorage.getToken();

  if (!token || !user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  const title = TITLES[location.pathname] || "LLM Cost Autopilot";

  function logout() {
    authStorage.clear();
    window.location.assign("/login");
  }

  return (
    <div className="flex h-screen bg-base-bg text-base-text font-sans">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <div className="flex items-center justify-between border-b border-base-border pr-6">
          <div className="min-w-0 flex-1">
            <TopBar title={title} />
          </div>
          <div className="flex items-center gap-3 pl-3">
            <span className="hidden text-sm text-base-subtext sm:inline">
              {user.name}
            </span>
            <button
              onClick={logout}
              className="rounded border border-base-border px-3 py-2 text-sm hover:bg-base-surface2"
            >
              Log out
            </button>
          </div>
        </div>

        <main className="flex-1 overflow-y-auto px-6 py-6">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/requests" element={<RequestsPage />} />
            <Route path="/routing" element={<Routing />} />
            <Route path="/models" element={<Models />} />
            <Route path="/budget" element={<Budget />} />
            <Route path="/try-it" element={<TryIt />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  const token = authStorage.getToken();
  const user = authStorage.getUser();
  const loggedIn = Boolean(token && user);

  return (
    <Routes>
      <Route
        path="/login"
        element={loggedIn ? <Navigate to="/" replace /> : <Login />}
      />
      <Route
        path="/signup"
        element={loggedIn ? <Navigate to="/" replace /> : <Signup />}
      />
      <Route path="/*" element={<ProtectedDashboard />} />
    </Routes>
  );
}