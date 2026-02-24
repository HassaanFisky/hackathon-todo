# Phase 1: Console Todo App

A pure Python in-memory console application for managing todo tasks, built with spec-driven development.

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) — Fast Python package manager

## Setup

```bash
# Clone the repository
git clone https://github.com/Hassaanfisky/hackathon-todo.git
cd hackathon-todo/phase1-console

# Install with uv (no dependencies to install — pure Python)
uv sync
```

## Run

```bash
uv run python src/main.py
```

## Commands

| Command    | Description             |
| ---------- | ----------------------- |
| `add`      | Add a new task          |
| `list`     | View all tasks          |
| `update`   | Update an existing task |
| `delete`   | Delete a task           |
| `complete` | Toggle task completion  |
| `help`     | Show available commands |
| `quit`     | Exit the application    |

## Example Session

```
Todo App > add
Title: Buy groceries
Description: Get milk and eggs
Task #1 added: Buy groceries

Todo App > list
1 ○ Buy groceries - Get milk and eggs

Todo App > complete
Task ID: 1
Task #1 marked as complete.

Todo App > list
1 ✓ Buy groceries - Get milk and eggs

Todo App > quit
Goodbye!
```

## Project Structure

```
phase1-console/
├── src/
│   └── main.py           # Entire application (single file)
├── specs/
│   └── phase1-console.md # Current specification
├── specs_history/
│   └── phase1-v1.md      # Archived spec version
├── CONSTITUTION.md        # Project rules & constraints
├── CLAUDE.md              # AI agent instructions
├── AGENTS.md              # Development methodology
├── README.md              # This file
├── pyproject.toml         # Project metadata
└── .python-version        # Python 3.13
```

## Methodology

This project follows **Spec-Driven Development**:

1. **Specify** → Define requirements in `specs/`
2. **Plan** → Break spec into steps
3. **Tasks** → Create testable tasks
4. **Implement** → Write code fulfilling the spec

See [AGENTS.md](AGENTS.md) and [CONSTITUTION.md](CONSTITUTION.md) for full details.
