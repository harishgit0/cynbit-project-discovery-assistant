# Cynbit Project Discovery & Scoping Assistant

An independent website-improvement prototype for a guided project inquiry. It is designed to complement Cynbit's existing discovery process by helping prospective clients describe their project goals, requirements, and planning expectations in a structured way.

## Current progress

The five-step Vue workflow, dynamic requirement choices, editable review, deterministic brief preview, FastAPI validation, idempotent inquiry endpoint, and PostgreSQL persistence are implemented. The frontend production build and local inquiry submission have been verified. The app is deployed publicly on Render and connected to Neon.

## Live demo

- Frontend: <https://cynbit-project-discovery-assistant-hz5m.onrender.com>
- API health: <https://cynbit-project-discovery-assistant.onrender.com/api/health>

## Repository layout

```text
frontend/            Vue 3 + Vite application
backend/app/         FastAPI application
backend/requirements.txt
```

The API uses PostgreSQL with structured inquiry columns and a JSONB requirements list. Its table is created on the first successful submission. Repeating a request with the same `Idempotency-Key` returns the original saved inquiry.

## API

- `GET /api/health` — API liveness check.
- `POST /api/inquiries` — validates an inquiry, generates a rule-based brief, and stores it in PostgreSQL.

The submit endpoint requires an `Idempotency-Key` UUID header. The frontend creates and reuses this key for retries in the current browser session.

## Local setup

Use Python 3.11 or later and Node.js 22.12 or later.

### Backend

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
notepad .env
# Add DATABASE_URL=<your PostgreSQL/Neon connection string>, then save and close Notepad.
uvicorn app.main:app --reload --env-file .env
```

The API health endpoint is `http://127.0.0.1:8000/api/health`. The real Neon connection string belongs in the ignored `backend/.env` file locally; never commit it.

### Frontend

In a second terminal, from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

The frontend uses `http://localhost:8000` by default. To change it, create `frontend/.env.local` with `VITE_API_BASE_URL` set to the API base URL.

## Environment variables

Backend deployment placeholders are listed in `.env.example`; frontend configuration is in `frontend/.env.example`. Keep real credentials in local environment variables or the hosting provider's secret settings. Do not commit `.env` files.

## Deploy with Render

The root `render.yaml` Blueprint defines a Python API service and a static Vue frontend. The current deployment is:

- Frontend: <https://cynbit-project-discovery-assistant-hz5m.onrender.com>
- API: <https://cynbit-project-discovery-assistant.onrender.com>

To recreate the deployment:

1. Push the repository to GitHub and connect it to Render.
2. In the Render Dashboard, create a new Blueprint and select this repository's `main` branch.
3. When prompted, provide `DATABASE_URL` from the local `backend/.env` file as a secret. Never add the connection string to Git.
4. Deploy both services and wait for their health/build checks to pass.

The API is configured in the Ohio region to stay near the Neon database's US East region. The frontend is served from Render's global static-site CDN. The free API service can spin down when idle; its first request afterward may take about a minute.

## Verification status

Verified: frontend production build; five-step wizard validation, category changes, back navigation, and review editing; local inquiry submission; public frontend HTTP response; public API health; CORS preflight from the deployed frontend; and idempotent API submission backed by a confirmed PostgreSQL row. Automated backend tests and a full form submission through the public browser remain to be checked.
