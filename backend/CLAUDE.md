# Backend Development

This is the FastAPI backend for the Hackathon Todo app.

## Setup

Use `uv` for managing dependencies.

```bash
uv sync
```

## Run

```bash
uv run uvicorn main:app --reload --port 8000
```

## Structure

- `main.py` - entry point
- `db.py` - database setup
- `models.py` - database models
- `auth.py` - authentication middleware
- `routes/` - API endpoints
