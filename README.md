# LLM Cost Autopilot

An LLM gateway and cost-management dashboard that routes prompts to configured language models based on prompt complexity, tracks token usage and estimated cost, and applies per-user usage and budget controls.

## Features

- **Prompt routing:** choose rule-based or LLM-based complexity classification (LOW, MEDIUM, HIGH).
- **Model selection:** map complexity levels to configured Gemini models when automatic routing is selected.
- **Chat playground:** send prompts and view the generated answer, selected model, complexity, routing reason, token usage, latency, and estimated cost.
- **Authentication:** signup/login with hashed passwords and JWT-protected API routes.
- **Usage analytics:** summary statistics, model usage, cost over time, recent requests, and routing-decision history.
- **Budget management:** configure a monthly budget, warning threshold, and restricted threshold.
- **Rate limiting:** enforce an hourly request limit using Redis.
- **Persistent records:** store users, model pricing, requests, and routing decisions in PostgreSQL.
- **Fast counters:** use Redis for daily/monthly usage counters and budget settings.
- **Evaluation and tests:** includes classifier/cost tests and routing evaluation scripts.

## Tech Stack

| Area | Technologies |
|---|---|
| Frontend | React, Vite, React Router, Recharts, Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| LLM provider | Google Gemini API (`google-genai`) |
| Database | PostgreSQL, SQLAlchemy, psycopg2 |
| Fast counters / rate limiting | Redis |
| Authentication | JWT (`PyJWT`), `pwdlib` password hashing |
| Testing | pytest |
| Local database setup | Docker Compose (PostgreSQL service) |

## Architecture

```text
React + Vite dashboard
        |
        | REST API + JWT
        v
FastAPI backend
  ├── Authentication
  ├── Rate limiting (Redis)
  ├── Budget enforcement
  ├── Complexity classifier
  │     ├── Rule-based classifier
  │     └── Gemini-based classifier
  ├── Model selector
  ├── Gemini response generation
  ├── Cost calculation
  └── Request / routing logging
        |
        ├── PostgreSQL: users, models, requests, routing decisions
        └── Redis: usage counters, budget settings, rate-limit counters
```

## Project Structure

```text
llm-cost-autopilot/
├── backend/
│   ├── app/
│   │   ├── api/          # Auth, chat, stats, usage, budget endpoints
│   │   ├── core/         # Settings and Redis client
│   │   ├── db/           # SQLAlchemy models and DB session
│   │   ├── providers/    # Gemini provider integration
│   │   ├── router/       # Complexity classifiers and model selector
│   │   └── services/     # Cost, budget, usage, rate limit, cache
│   ├── eval/             # Routing evaluation scripts and datasets
│   ├── tests/            # Unit tests
│   ├── requirements.txt
│   └── seed.py           # Initializes model catalog/pricing
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── api.js
│       │   └── useApi.js
│       └── package.json
├── docker-compose.yml
└── README.md
```

## Requirements

- Python 3.11+ recommended
- Node.js and npm
- PostgreSQL 16, either installed locally or run with Docker Compose
- Redis
- A Google Gemini API key

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd llm-cost-autopilot
```

Replace the placeholder URL with your repository URL.

### 2. Start PostgreSQL

You can use the included Docker Compose configuration to start PostgreSQL:

```bash
docker compose up -d postgres
```

The current Compose configuration creates a local database named `autopilot` with the development user `autopilot`. Change these development credentials before using this setup beyond local development.

If you already run PostgreSQL locally, create a database and user and use their connection URL in the backend environment variables.

### 3. Start Redis

Redis must be running and reachable at the URL configured in `REDIS_URL`.

For example, a local Redis instance commonly uses:

```text
redis://localhost:6379/0
```

The included Docker Compose file starts PostgreSQL only; it does not start Redis, the backend, or the frontend.

### 4. Configure the backend

Open a terminal in the `backend` directory and create a `.env` file. Do not commit this file.

```env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/autopilot
GEMINI_API_KEY=your_gemini_api_key
DEFAULT_MODEL=gemini-3.6-flash
REDIS_URL=redis://localhost:6379/0
MONTHLY_BUDGET=5.00
JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

- Replace `USER` and `PASSWORD` with your PostgreSQL credentials.
- Replace `your_gemini_api_key` with your Gemini API key.
- Use a long, random `JWT_SECRET_KEY`; do not use a sample value in production.
- Ensure the model name is available to your Gemini API account.
- Keep provider keys and secrets on the backend only.

### 5. Install backend dependencies

From the `backend` directory:

**Windows PowerShell**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### 6. Initialize database tables and model records

From the `backend` directory, with the virtual environment activated and `.env` configured:

```bash
python seed.py
```

The seed script creates database tables and inserts or updates the configured model catalog and token prices.

**Important:** Review `backend/seed.py` before using the cost dashboard. The seed file itself notes that model prices should be replaced with current prices for the applicable provider tier. Prices and model availability can change; the dashboard's cost estimates depend on these values.

### 7. Configure and start the frontend

Open a second terminal in `frontend/frontend`.

Create a `.env` file:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Install dependencies and start Vite:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite (commonly `http://localhost:5173`).

### 8. Start the backend

Open a terminal in `backend`, activate its virtual environment, and run:

```bash
python -m uvicorn app.main:app --reload
```

API base URL: `http://127.0.0.1:8000`

Interactive API docs: `http://127.0.0.1:8000/docs`

Run PostgreSQL and Redis before using authenticated chat and usage features.

## Using the Application

1. Open the frontend and create an account.
2. Log in.
3. Open **Try it**, enter a prompt, and choose the rule-based or LLM-based router.
4. Review the answer, selected model, complexity, latency, tokens, and estimated cost.
5. Open **Overview** to inspect usage summaries and cost charts.
6. Open **Requests** and **Routing** to inspect recorded requests and routing decisions.
7. Open **Models** to inspect configured model pricing.
8. Open **Budget** to configure the monthly limit and thresholds.

## API Endpoints

The API is documented interactively at `/docs`. Principal routes include:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/signup` | Create an account |
| `POST` | `/auth/login` | Log in and receive a JWT |
| `POST` | `/v1/chat` | Generate a response through the routing pipeline |
| `GET` | `/v1/stats/summary` | Aggregate usage statistics |
| `GET` | `/v1/stats/model-usage` | Usage grouped by model |
| `GET` | `/v1/stats/cost-over-time` | Cost over time |
| `GET` | `/v1/stats/requests` | Recent request history |
| `GET` | `/v1/stats/routing-decisions` | Routing-decision history |
| `GET` | `/v1/stats/models` | Configured model catalog |
| `GET` | `/v1/usage/today` | Today's usage counters |
| `GET` | `/v1/budget` | Current budget status |
| `PUT` | `/v1/budget/limit` | Update monthly budget |
| `PUT` | `/v1/budget/warning-threshold` | Update warning threshold |
| `PUT` | `/v1/budget/restricted-threshold` | Update restricted threshold |
| `GET` | `/health` | Health check |

Protected routes require the JWT in the `Authorization: Bearer <token>` header.

## How Cost Is Estimated

The cost service estimates each request using the model's configured input and output prices per million tokens:

```text
estimated_cost =
  (input_tokens * input_price_per_1M
   + output_tokens * output_price_per_1M) / 1,000,000
```

This is an estimate based on the stored price catalog and token usage returned by the provider. Verify pricing, model availability, and provider billing rules before relying on the values for financial reporting.

## Tests and Evaluation

From the `backend` directory, activate the virtual environment and run:

```bash
pytest
```

The `backend/eval/` directory contains scripts and prompt data for evaluating routing/classification behavior. Inspect its scripts and datasets for the exact evaluation procedure before running them.

## Security Notes

- **Never commit `.env` files, API keys, database passwords, JWT secrets, access tokens, or real user data.**
- Keep `GEMINI_API_KEY` on the backend; do not expose it through Vite variables.
- Use a unique, randomly generated JWT secret in any shared deployment.
- Change the development PostgreSQL credentials in `docker-compose.yml` before deployment.
- The frontend stores the JWT in browser storage in the current implementation. Review the authentication design and XSS protections before deploying to production.
- The included Compose file runs PostgreSQL only. Configure Redis and the backend separately.
- This project is a development/demo implementation; add production-grade monitoring, secret management, backups, concurrency-safe budget enforcement, and deployment hardening before exposing it publicly.

## Current Scope and Limitations

- The supplied provider integration is for Google Gemini.
- Automatic model selection uses the configured classifier-to-model mapping; verify the selected model names and pricing records in your environment.
- The Redis cache service exists, but it should not be described as active response caching unless it is connected to the chat request pipeline.
- Cost figures are estimates based on token counts and the price records configured in the database.
- Budget enforcement is application-level and should be tested under concurrent requests before production use.

## License

No license is specified yet. Add a `LICENSE` file and update this section if you intend to distribute the project under an open-source license.
