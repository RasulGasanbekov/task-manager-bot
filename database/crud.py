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

