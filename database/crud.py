from .models import Task
from . import SessionLocal

def create_task(user_id, title, deadline, category, priority):
    session = SessionLocal()
    task = Task(
        user_id=user_id,
        title=title,
        deadline=deadline,
        category=category,
        priority=priority
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    session.close()
    return task

def get_tasks_by_user(user_id):
    session = SessionLocal()
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    session.close()
    return tasks

def update_task_status(task_id: int, new_status: str):
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = new_status
            db.commit()

def get_task_by_id(user_id: int, task_id: int):
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
        return task