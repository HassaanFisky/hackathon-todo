"""
mcp_server.py — Task tool functions used by the Gemini Agent.
Each function maps to a Gemini function declaration and performs
direct DB operations using SQLModel sync sessions.
"""
from datetime import datetime
from sqlmodel import Session, select
from db import engine
from models import Task


def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task in the database for the given user."""
    with Session(engine) as session:
        task = Task(user_id=user_id, title=title, description=description or "")
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "created", "title": task.title}


def list_tasks(user_id: str, status: str = "all") -> list:
    """Return tasks for a user, optionally filtered by completion status."""
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)
        query = query.order_by(Task.created_at.desc())
        tasks = session.exec(query).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description or "",
                "completed": t.completed,
                "created_at": t.created_at.isoformat(),
            }
            for t in tasks
        ]


def complete_task(user_id: str, task_id: int) -> dict:
    """Toggle completed status of a task. Returns new status."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"error": "Task not found"}
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        new_status = "completed" if task.completed else "incomplete"
        return {"task_id": task.id, "status": new_status, "title": task.title}


def delete_task(user_id: str, task_id: int) -> dict:
    """Delete a task from the database."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"error": "Task not found"}
        title = task.title
        session.delete(task)
        session.commit()
        return {"task_id": task_id, "status": "deleted", "title": title}


def update_task(
    user_id: str,
    task_id: int,
    title: str = None,
    description: str = None,
) -> dict:
    """Update a task's title and/or description."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"error": "Task not found"}
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "updated", "title": task.title}
