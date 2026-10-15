# Collaborative Dashboard

A Trello-like board app: users create boards with columns and tasks, invite members,
and see each other's changes live.

- **Frontend:** React + TypeScript (Vite) — `frontend/`
- **Backend:** Python FastAPI + SQLAlchemy + Alembic — `backend/`
- **Database:** PostgreSQL (Docker)

## Running locally

Requirements: Docker Desktop, [uv](https://docs.astral.sh/uv/), Node.js.

```powershell
# 1. Database (from the project root)
docker compose up -d

# 2. Backend
cd backend
copy .env.example .env
uv sync
uv run alembic upgrade head
uv run fastapi dev          # http://localhost:8000, API docs at /docs

# 3. Frontend (in another terminal)
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

## Migrations

```powershell
uv run alembic revision --autogenerate -m "describe the change"   # then read the generated file!
uv run alembic upgrade head
uv run alembic check        # models and DB in sync?
```
