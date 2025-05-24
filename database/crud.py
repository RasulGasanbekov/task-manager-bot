from .models import Task
from . import SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


def create_task(user_id, title, deadline, category, priority):
    with SessionLocal() as db:
        task = Task(
            user_id=user_id,
            title=title,
            deadline=deadline,
            category=category,
            priority=priority,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task


def update_task(task_id: int, **kwargs):
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            db.commit()
            db.refresh(task)
        return task


def update_task_reminder(task_id: int, reminder_days: int):
    """
    Обновляет поле reminder_days для задачи с указанным ID
    """
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.reminder_days = reminder_days
            db.commit()
            db.refresh(task)
        return task


def get_tasks_by_deadline_range(user_id: int, start: datetime, end: datetime):
    with SessionLocal() as db:
        return (
            db.query(Task)
            .filter(Task.user_id == user_id, Task.deadline.between(start, end))
            .order_by(Task.deadline)
            .all()
        )


def get_tasks_by_user(user_id):
    with SessionLocal() as db:
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        return tasks


def update_task_status(task_id: int, new_status: str):
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = new_status
            db.commit()


def get_task_by_id(task_id: int):
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        return task


def delete_task(task_id: int):
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()


def get_tasks_with_due_reminder(today: datetime.date):
    """
    Возвращает задачи, у которых сегодня = deadline - reminder_days
    """
    session = SessionLocal()
    tasks = session.query(Task).all()
    result = []

    for task in tasks:
        if task.reminder_days <= 0:
            continue
        reminder_date = task.deadline - timedelta(days=task.reminder_days)
        if reminder_date.date() == today:
            result.append(task)

    return result


def get_tasks_by_filters(
    user_id: int,
    category: str,
    priority: str,
    status: str = None,
    start: datetime = None,
    end: datetime = None,
):
    with SessionLocal() as db:
        query = db.query(Task).filter(Task.user_id == user_id)

        if category and category != "все":
            query = query.filter(Task.category == category)
        if priority and priority != "any":
            query = query.filter(Task.priority == priority)
        if status:
            query = query.filter(Task.status == status)
        if start:
            query = query.filter(Task.deadline >= start)
        if end:
            query = query.filter(Task.deadline <= end)

        return query.order_by(Task.deadline).all()
