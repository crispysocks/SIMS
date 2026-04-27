# AGENTS.md

## Project Overview

FastAPI Student Management System (SIMS). Python 3.12 + SQLAlchemy + MySQL.

## Commands

- **Dev server**: `uv run fastapi dev` or `uv run uvicorn app.main:app --reload`
- **Tests**: `uv run pytest`
- **Sync deps**: `uv sync`

## Database

- MySQL, database `student_management`. Auto-creates on startup via `app/core/database.py`.
- Config in `.env` (see `.env.example`). Key vars: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `CORS_ORIGINS` (JSON string), `UPLOAD_DIR`.
- Default CORS: `http://localhost:5173` only.

## Architecture

- `app/` is root package. Use `from app.core.config import settings` (not `from app.config`).
- Entry point: `app/main.py` (includes all routers on startup, calls `init_db()`).
- Auth: Header-based (`X-User`, `X-Roles`). Default roles: `admin`, `teacher`. See `app/dependencies.py`.

## Key Files

- `app/core/config.py` — Settings class with `case_sensitive=True` (env vars must be UPPER_SNAKE_CASE).
- `app/core/database.py` — Engine, SessionLocal, get_db, init_db.
- `app/api/` — All route modules.
- `app/models/` — SQLAlchemy models.
- `app/schemas/` — Pydantic schemas.

## Quirks

- Upload path `./uploads` hardcoded in some services — directory doesn't exist by default, create it if needed.
- Excel import expects columns matching `Student` model fields (`student_no`, `name`, `gender`, `grade`, etc.).