# AGENTS.md

## Project Overview

FastAPI Student Management System (SIMS). Single-package Python project with `app/` as the main module.

## Python & Toolchain

- **Python 3.12** required (`.python-version`). Use `uv` for dependency management.
- No `uv.lock` entry points defined — `uv run fastapi dev` or `uv run uvicorn app.main:app --reload` is the typical dev start.
- No tests, no lint config, no pre-commit hooks.

## App Architecture

- `app/` is the root package. All imports go through it (e.g., `from app.core.config import settings`, not `from app.core.database import ...`).
- **Existing stub modules that import wrong** — `app/core/database.py` imports `from app.config import settings` (should be `app.core.config`). `app/services/student.py` imports `from app.database import get_db` and `from app.dependencies import get_current_user, require_role` (neither module exists yet). When building out these features, fix imports to match the actual file locations.
- `app/main.py` is empty. Add `app` routers here.
- Empty but referenced packages to implement: `app/models/`, `app/schemas/`, `app/api/`, `app/dependencies.py`, `app/utils/`.

## Database

- MySQL, database name `student_management`. Configured in `app/core/config.py` via `Settings`.
- Default MySQL credentials in config: `root` / `your_password`. Override with a `.env` file (loaded automatically by Pydantic Settings).
- `app/core/database.py` creates the SQLAlchemy engine and `SessionLocal` / `get_db`.

## Configuration

- Settings class in `app/core/config.py` with `case_sensitive=True` (all env vars must be UPPER_SNAKE_CASE).
- Key settings: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `CORS_ORIGINS` (JSON string), `UPLOAD_DIR`, `MAX_FILE_SIZE`.
- CORS default allows only `http://localhost:5173`.

## Development Quirks

- Upload path in `app/services/student.py` hardcodes `./backend/uploads/` — this directory does not exist by default.
- Excel import expects columns matching `Student` model fields directly (e.g., `student_no`, `name`, `gender`, `grade`, etc.).
