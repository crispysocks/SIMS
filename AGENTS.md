# AGENTS.md

## Project Overview

FastAPI Student Management System (SIMS). Python 3.12 + SQLAlchemy + MySQL + React 19 + TypeScript.

## Commands

### 后端
- **Dev server**: `uv run fastapi dev` or `uv run uvicorn app.main:app --reload`
- **Tests**: `uv run pytest`
- **Sync deps**: `uv sync`

### 前端
- **Dev server**: `cd frontend && npm run dev`
- **Build**: `cd frontend && npm run build`
- **Lint**: `cd frontend && npm run lint`

## Database

- MySQL, database `student_management`. Auto-creates on startup via `app/core/database.py`.
- Config in `.env` (see `.env.example`). Key vars: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `CORS_ORIGINS` (JSON string), `UPLOAD_DIR`.
- Default CORS: `http://localhost:5173` only.

## Architecture

### 后端
- `app/` is root package. Use `from app.core.config import settings` (not `from app.config`).
- Entry point: `app/main.py` (includes all routers on startup, calls `init_db()`).
- Auth: Header-based (`X-User`, `X-Roles`). Default roles: `admin`, `teacher`. See `app/dependencies.py`.

### 前端
- Entry point: `frontend/src/main.tsx`
- Routes: `frontend/src/routes/index.tsx`
- API client: `frontend/src/api/client.ts` (Axios with interceptors for auth headers)
- State management: Zustand with persist middleware (`authStore`, `appStore`)
- Data fetching: TanStack Query v5
- UI components: Custom shadcn/ui-style components in `frontend/src/components/ui/`

## Key Files

### 后端
- `app/core/config.py` — Settings class with `case_sensitive=True` (env vars must be UPPER_SNAKE_CASE).
- `app/core/database.py` — Engine, SessionLocal, get_db, init_db.
- `app/api/` — All route modules.
- `app/models/` — SQLAlchemy models.
- `app/schemas/` — Pydantic schemas.

### 前端
- `frontend/src/api/` — API modules per domain (students, teachers, classes, scores, employment, statistics).
- `frontend/src/types/` — TypeScript interfaces for all entities.
- `frontend/src/stores/` — Zustand stores (auth, app UI state).
- `frontend/src/lib/constants.ts` — Role permissions, enum mappings.

## Quirks

- Upload path `./uploads` hardcoded in some services — directory doesn't exist by default, create it if needed.
- Excel import expects columns matching `Student` model fields (`student_no`, `name`, `gender`, `grade`, etc.).
- Frontend uses no pagination — all data is fetched and scrollable in tables.
- API response format varies: some return `{message, data}`, others return model directly. Client interceptor normalizes this.
