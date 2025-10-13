# app/tasks/jobs.py
from time import sleep
from celery import shared_task
from sqlalchemy.orm import Session
from db.session import sessionlocal

@shared_task
def long_running_task(n: int) -> int:
    total = 0
    for i in range(n):
        sleep(1)
        total += i
    return total

@shared_task
def count_users_task() -> int:
    db: Session = sessionlocal()
    try:
        from models.user import User
        return db.query(User).count()
    finally:
        db.close()
