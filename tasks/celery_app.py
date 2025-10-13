import os
from celery import Celery
from core.config import settings

celery_app = Celery(
    "app",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.task_acks_late = True
celery_app.conf.result_expires = 3600
