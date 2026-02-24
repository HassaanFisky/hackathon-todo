# Hackathon Todo - Development Context

## Structure

- `backend/`: FastAPI + SQLModel + PostgreSQL (neon)
- `frontend/`: Next.js 16+ + TailwindCSS + Better Auth
- `specs/`: Markdown specification files

## Spec-Kit

- Configured using `.spec-kit/config.yaml`
- Use this to track different components and phases.

## Workflow

1. Read specs first.
2. Develop backend logic and models.
3. Test backend logic.
4. Integrate with the Next.js App Router.

## Commands

- **Backend**: `cd backend && uv run uvicorn main:app --reload --port 8000`
- **Frontend**: `cd frontend && npm run dev`
- **Docker**: `docker-compose up --build`
