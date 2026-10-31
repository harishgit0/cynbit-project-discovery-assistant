# Cynbit Project Discovery & Scoping Assistant

An independent website-improvement prototype for a guided project inquiry. It is designed to complement Cynbit's existing discovery process by helping prospective clients describe their project goals, requirements, and planning expectations in a structured way.

## Current progress

The five-step Vue workflow, dynamic requirement choices, editable review, deterministic brief preview, FastAPI validation, idempotent inquiry endpoint, and PostgreSQL persistence code are implemented. The local API, database connection, automated tests, deployment, and complete public submission flow still need to be run and verified.

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
uvicorn app.main:app --reload
```

The API health endpoint is `http://127.0.0.1:8000/api/health`. Set `DATABASE_URL` in the backend process environment to enable inquiry submissions. The connection string should use SSL when required by the PostgreSQL host.

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

## Verification status

The application has not yet been run end to end from this fresh checkout. Treat setup as verified only after starting both servers, connecting a PostgreSQL database, and completing a public or local inquiry submission. Automated backend tests and deployment verification are pending.
