# Phase 1 Specification: Console Todo App

## Overview

A pure Python in-memory console application for managing todo tasks. All data is stored in-memory only — no database, no file persistence.

## Data Model

Each task is a dictionary with the following fields:

| Field         | Type   | Description                                   |
| ------------- | ------ | --------------------------------------------- |
| `id`          | `int`  | Auto-increment starting from 1                |
| `title`       | `str`  | Task title (required)                         |
| `description` | `str`  | Task description (optional, defaults to `""`) |
| `completed`   | `bool` | Completion status (defaults to `False`)       |
| `created_at`  | `str`  | ISO timestamp from `datetime.now()`           |

---

## Features

### Feature 1: Add Task

- **Command**: `add`
- **Input**: Title (required), Description (optional)
- **Behavior**:
  - Prompts the user for a title (required — cannot be empty).
  - Prompts the user for a description (optional — can be empty).
  - System assigns an auto-increment ID starting from 1.
  - Sets `completed` to `False`.
  - Sets `created_at` to `datetime.now()` in ISO format.
- **Output**: `Task #[ID] added: [title]`

### Feature 2: View All Tasks

- **Command**: `list`
- **Behavior**:
  - Displays all tasks in the format: `[ID] [✓/○] [title] - [description]`
  - `✓` indicates completed tasks, `○` indicates pending tasks.
  - If no tasks exist, display: `No tasks found.`
- **Output Example**:
  ```
  1 ○ Buy groceries - Get milk and eggs
  2 ✓ Read book - Finish chapter 5
  ```

### Feature 3: Update Task

- **Command**: `update`
- **Input**: Task ID, new title, new description
- **Behavior**:
  - Prompts for the task ID.
  - Validates that the ID exists. If not: `Task not found.`
  - Prompts for a new title (press Enter to keep current).
  - Prompts for a new description (press Enter to keep current).
- **Output**: `Task #[ID] updated.`

### Feature 4: Delete Task

- **Command**: `delete`
- **Input**: Task ID
- **Behavior**:
  - Prompts for the task ID.
  - Validates that the ID exists. If not: `Task not found.`
  - Removes the task from the in-memory list.
- **Output**: `Task #[ID] deleted.`

### Feature 5: Mark Complete / Incomplete

- **Command**: `complete`
- **Input**: Task ID
- **Behavior**:
  - Prompts for the task ID.
  - Validates that the ID exists. If not: `Task not found.`
  - Toggles the `completed` field.
    - If `False` → set to `True`, output: `Task #[ID] marked as complete.`
    - If `True` → set to `False`, output: `Task #[ID] marked as incomplete.`

### Feature 6: Help

- **Command**: `help`
- **Behavior**: Displays a list of all available commands with brief descriptions.
- **Output**:
  ```
  Available commands:
    add      - Add a new task
    list     - View all tasks
    update   - Update an existing task
    delete   - Delete a task
    complete - Toggle task completion
    help     - Show this help message
    quit     - Exit the application
  ```

### Feature 7: Quit

- **Command**: `quit`
- **Behavior**: Exits the application cleanly.
- **Output**: `Goodbye!`

---

## Error Handling

- **Empty input**: Ignore and re-prompt.
- **Invalid command**: Display `Unknown command. Type "help" for available commands.`
- **Invalid ID (non-numeric)**: Display `Invalid ID. Please enter a number.`
- **Non-existent ID**: Display `Task not found.`
- **Empty title on add**: Re-prompt with `Title cannot be empty.`

---

## Constraints

- Pure Python 3.13, no external packages.
- Single file: `src/main.py`.
- All data in-memory only.
- PEP 8 compliant with type hints and docstrings.
