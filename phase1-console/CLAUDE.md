# CLAUDE

## Project Context

This is **Phase I** of the Hackathon Todo App — a pure Python in-memory console application.

## Key Files

- `src/main.py` — Entire application (single file)
- `specs/phase1-console.md` — Current specification
- `specs_history/` — Archived spec versions
- `CONSTITUTION.md` — Project rules and constraints
- `AGENTS.md` — Development methodology

## Rules for AI Agents

1. Read `CONSTITUTION.md` before making any changes.
2. Read `AGENTS.md` to understand the spec-driven workflow.
3. Read `specs/phase1-console.md` for current feature requirements.
4. Do not add features not defined in the spec.
5. Do not introduce external dependencies.
6. Maintain PEP 8, type hints, and docstrings on all functions.
7. All data must remain in-memory — no files, no databases.

## Run Command

```bash
uv run python src/main.py
```
