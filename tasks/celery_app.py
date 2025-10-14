from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",      # for local Redis; change as needed
    backend="redis://localhost:6379/0"
)
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)
