# Cynbit Project Discovery & Scoping Assistant

An independent website-improvement prototype for a guided project inquiry. It is designed to complement Cynbit's existing discovery process by helping prospective clients describe their project goals, requirements, and planning expectations in a structured way.

## Current progress

The repository currently contains the Vue/Vite frontend shell and a minimal FastAPI health endpoint. The five-step inquiry workflow, database integration, deployment, and technical assessment report remain to be implemented and verified.

## Repository layout

```text
frontend/            Vue 3 + Vite application
backend/app/         FastAPI application
backend/requirements.txt
```

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

The API health endpoint is `http://127.0.0.1:8000/api/health`.

### Frontend

In a second terminal, from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

The frontend uses `http://localhost:8000` by default. To change it, create `frontend/.env.local` with `VITE_API_BASE_URL` set to the API base URL.

## Environment variables

Backend deployment placeholders are listed in `.env.example`. Keep real credentials in local environment variables or the hosting provider's secret settings. Do not commit `.env` files.

## Verification status

The application has not yet been run end to end from this fresh checkout. Treat setup as verified only after starting both servers and seeing the frontend report that the API is connected.
