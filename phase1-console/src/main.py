"""
Phase 1: In-Memory Console Todo App

A pure Python console application for managing todo tasks.
All data is stored in-memory only — no database, no file persistence.

Spec Reference: specs/phase1-console.md
"""

from datetime import datetime


# ---------------------------------------------------------------------------
# Global State
# ---------------------------------------------------------------------------
tasks: list[dict] = []
next_id: int = 1


# ---------------------------------------------------------------------------
# Task Operations
# ---------------------------------------------------------------------------

def find_task(task_id: int) -> dict | None:
    """Find and return a task by its ID, or None if not found.

    Args:
        task_id: The integer ID of the task to find.

    Returns:
        The task dictionary if found, otherwise None.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def add_task() -> None:
    """Add a new task to the in-memory task list.

    Prompts the user for a title (required) and description (optional).
    Assigns an auto-increment ID, sets completed to False, and records
    the current timestamp as created_at.

    Spec: Feature 1 — Add Task
    """
    global next_id

    title: str = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    description: str = input("Description: ").strip()

    task: dict = {
        "id": next_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }

    tasks.append(task)
    print(f"Task #{next_id} added: {title}")
    next_id += 1


def list_tasks() -> None:
    """Display all tasks in a formatted list.

    Format: [ID] [✓/○] [title] - [description]
    ✓ = completed, ○ = pending.
    If no tasks exist, prints 'No tasks found.'

    Spec: Feature 2 — View All Tasks
    """
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status: str = "✓" if task["completed"] else "○"
        desc: str = f" - {task['description']}" if task["description"] else ""
        print(f"{task['id']} {status} {task['title']}{desc}")


def update_task() -> None:
    """Update the title and/or description of an existing task.

    Prompts for the task ID, validates existence, then prompts for
    new title and description. Press Enter to keep the current value.

    Spec: Feature 3 — Update Task
    """
    raw_id: str = input("Task ID: ").strip()

    try:
        task_id: int = int(raw_id)
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    task: dict | None = find_task(task_id)
    if task is None:
        print("Task not found.")
        return

    new_title: str = input(f"New title (Enter to keep '{task['title']}'): ").strip()
    new_desc: str = input(
        f"New description (Enter to keep '{task['description']}'): "
    ).strip()

    if new_title:
        task["title"] = new_title
    if new_desc:
        task["description"] = new_desc

    print(f"Task #{task_id} updated.")


def delete_task() -> None:
    """Delete a task by its ID.

    Prompts for the task ID, validates existence, then removes the
    task from the in-memory list.

    Spec: Feature 4 — Delete Task
    """
    raw_id: str = input("Task ID: ").strip()

    try:
        task_id: int = int(raw_id)
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    task: dict | None = find_task(task_id)
    if task is None:
        print("Task not found.")
        return

    tasks.remove(task)
    print(f"Task #{task_id} deleted.")


def toggle_complete() -> None:
    """Toggle the completed status of a task.

    Prompts for the task ID, validates existence, then flips the
    completed boolean. Outputs the new status.

    Spec: Feature 5 — Mark Complete / Incomplete
    """
    raw_id: str = input("Task ID: ").strip()

    try:
        task_id: int = int(raw_id)
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    task: dict | None = find_task(task_id)
    if task is None:
        print("Task not found.")
        return

    task["completed"] = not task["completed"]

    if task["completed"]:
        print(f"Task #{task_id} marked as complete.")
    else:
        print(f"Task #{task_id} marked as incomplete.")


def show_help() -> None:
    """Display all available commands with brief descriptions.

    Spec: Feature 6 — Help
    """
    print("Available commands:")
    print("  add      - Add a new task")
    print("  list     - View all tasks")
    print("  update   - Update an existing task")
    print("  delete   - Delete a task")
    print("  complete - Toggle task completion")
    print("  help     - Show this help message")
    print("  quit     - Exit the application")


# ---------------------------------------------------------------------------
# Command Dispatch
# ---------------------------------------------------------------------------

COMMANDS: dict[str, callable] = {
    "add": add_task,
    "list": list_tasks,
    "update": update_task,
    "delete": delete_task,
    "complete": toggle_complete,
    "help": show_help,
}


# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the main application loop.

    Continuously prompts for user input, dispatches to the appropriate
    command handler, and exits cleanly on 'quit'.

    Spec: Feature 7 — Quit + continuous input loop
    """
    print("=" * 40)
    print("  Hackathon Todo App — Phase I")
    print("  Type 'help' for available commands")
    print("=" * 40)

    while True:
        try:
            command: str = input("\nTodo App > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not command:
            continue

        if command == "quit":
            print("Goodbye!")
            break

        handler = COMMANDS.get(command)
        if handler:
            handler()
        else:
            print('Unknown command. Type "help" for available commands.')


if __name__ == "__main__":
    main()
