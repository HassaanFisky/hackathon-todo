from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from db import engine
from auth import get_current_user_id
from models import Task

router = APIRouter(prefix="/api", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/{user_id}/tasks", response_model=List[Task])
def get_tasks(user_id: str, status: Optional[str] = None, sort: Optional[str] = None, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these tasks")
    
    query = select(Task).where(Task.user_id == user_id)
    if status == "completed":
        query = query.where(Task.completed == True)
    elif status == "pending":
        query = query.where(Task.completed == False)
        
    if sort == "asc":
        query = query.order_by(Task.created_at.asc())
    else:
        query = query.order_by(Task.created_at.desc())
        
    results = session.exec(query).all()
    return results

@router.post("/{user_id}/tasks", response_model=Task)
def create_task(user_id: str, task: TaskCreate, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    new_task = Task(user_id=user_id, title=task.title, description=task.description)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

@router.get("/{user_id}/tasks/{id}", response_model=Task)
def get_task(user_id: str, id: int, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    task = session.get(Task, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return task

@router.put("/{user_id}/tasks/{id}", response_model=Task)
def update_task(user_id: str, id: int, task_update: TaskUpdate, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    task = session.get(Task, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
        
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{user_id}/tasks/{id}")
def delete_task(user_id: str, id: int, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    task = session.get(Task, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
        
    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}

@router.patch("/{user_id}/tasks/{id}/complete", response_model=Task)
def toggle_completion(user_id: str, id: int, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    task = session.get(Task, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
