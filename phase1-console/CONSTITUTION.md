# CONSTITUTION

## Project: Hackathon Todo Console App

### Phase I: In-Memory Python Console App

---

## Core Principles

1. **In-Memory Only**: All data is stored in-memory only. No database, no file I/O, no persistence layer of any kind. When the application exits, all data is lost.

2. **Code Standards**:
   - PEP 8 compliant
   - Type hints on all function signatures
   - Docstrings on all functions
   - Clean, readable, maintainable code

3. **Task Data Model**:
   Each task is a dictionary with the following fields:
   | Field        | Type     | Description                              |
   |--------------|----------|------------------------------------------|
   | `id`         | `int`    | Auto-increment starting from 1           |
   | `title`      | `str`    | Task title (required)                    |
   | `description`| `str`    | Task description (optional, default: "") |
   | `completed`  | `bool`   | Completion status (default: False)       |
   | `created_at` | `str`    | ISO timestamp via `datetime.now()`       |

4. **Single File Architecture**: All application code resides in `src/main.py`. No modules, no packages, no splitting.

5. **Zero External Dependencies**: Pure Python standard library only. No pip packages, no third-party imports.

6. **Spec-Driven Development**: Every feature must trace back to a specification document. No features beyond spec.
