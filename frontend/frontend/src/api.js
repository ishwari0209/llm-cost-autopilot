
const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const authStorage = {
  getToken: () => localStorage.getItem("access_token"),
  getUser: () => {
    try {
      return JSON.parse(localStorage.getItem("auth_user") || "null");
    } catch {
      return null;
    }
  },
  save: (data) => {
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("auth_user", JSON.stringify(data.user));
  },
  clear: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("auth_user");
  },
};

async function request(path, options = {}) {
  let res;
  const token = authStorage.getToken();

  try {
    res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
      },
    });
  } catch {
    throw new Error(`Could not reach API at ${BASE_URL}. Is the backend running?`);
  }

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") {
        detail = body.detail;
      } else if (body.detail) {
        detail = JSON.stringify(body.detail);
      } else {
        detail = JSON.stringify(body);
      }
    } catch {}

    // If an authenticated API call is rejected, clear the stale session.
    // Do not redirect for failed login/signup attempts.
    if (
      res.status === 401 &&
      token &&
      !path.startsWith("/auth/login") &&
      !path.startsWith("/auth/signup")
    ) {
      authStorage.clear();
      if (window.location.pathname !== "/login") {
        window.location.assign("/login");
      }
    }

    const error = new Error(`${res.status}: ${detail}`);
    error.status = res.status;
    throw error;
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  signup: (payload) =>
    request("/auth/signup", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  login: (payload) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  summary: () => request("/v1/stats/summary"),
  modelUsage: () => request("/v1/stats/model-usage"),
  costOverTime: (days = 14) => request(`/v1/stats/cost-over-time?days=${days}`),
  requests: (limit = 50) => request(`/v1/stats/requests?limit=${limit}`),
  routingDecisions: (limit = 50) =>
    request(`/v1/stats/routing-decisions?limit=${limit}`),
  models: () => request("/v1/stats/models"),
  usageToday: () => request("/v1/usage/today"),
  budget: () => request("/v1/budget"),

  setBudgetLimit: (amount) =>
    request("/v1/budget/limit", {
      method: "PUT",
      body: JSON.stringify({ amount }),
    }),

  setWarningThreshold: (percent) =>
    request("/v1/budget/warning-threshold", {
      method: "PUT",
      body: JSON.stringify({ percent }),
    }),

  setRestrictedThreshold: (percent) =>
    request("/v1/budget/restricted-threshold", {
      method: "PUT",
      body: JSON.stringify({ percent }),
    }),

  chat: (payload) =>
    request("/v1/chat", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};