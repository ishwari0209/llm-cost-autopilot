# LLM Cost Autopilot — Dashboard

React + Vite + Tailwind + Recharts frontend for the LLM Cost Autopilot backend.

## Setup

```bash
cd frontend
npm install
npm run dev
```

Opens at http://localhost:5173.

Make sure your FastAPI backend is running first (`uvicorn app.main:app --reload`
from the `backend/` folder), and that CORS is enabled there for
`http://localhost:5173` (see `main.py`).

## Configuration

The API base URL is read from `.env`:

```
VITE_API_URL=http://127.0.0.1:8000
```

Change this when deploying — never hardcode the URL in code.

## Pages

- **Overview** — total requests/tokens/cost/latency, cost-over-time chart,
  model usage breakdown, live "today" counter (polls every 10s)
- **Requests** — table of the last 50 requests with tokens, cost, latency, status
- **Routing** — every routing decision with complexity score/level and the
  reason the router gave
- **Models** — configured models and their per-1M-token pricing
- **Budget** — current spend vs. limit, with editable limit/warning/restricted
  thresholds that save instantly via the API (no backend restart needed)
- **Try it** — send a prompt live through the gateway and see the full routed
  response: model used, complexity classification, cost, latency, and any
  fallback that occurred

## Required backend endpoints

See `src/api.js` for the full list this dashboard calls. All of them need to
exist on the FastAPI backend: `/v1/stats/*`, `/v1/usage/today`, `/v1/budget`
(GET + 3 PUT routes), and `/v1/chat`.
