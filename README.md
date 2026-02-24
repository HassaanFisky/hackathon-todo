# Hackathon Todo App

## Phase I

Pure Python console app storing data in memory.

```bash
cd phase1-console
uv sync
uv run python src/main.py
```

## Phase II

Full-Stack Web Application built with Next.js, FastAPI, SQLModel, and PostgreSQL (via Neon).
Authentication is managed via Better Auth.

### Architecture

- Frontend: `Next.js App Router (localhost:3000)`
- Backend: `FastAPI (localhost:8000)`
- Database: `PostgreSQL Database (Neon)`

### Setup & Run

Make sure `backend/.env` and `frontend/.env.local` are created correctly.

#### Backend

```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Run with Docker

```bash
docker-compose up --build
```
