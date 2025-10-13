# app/api/routes_tasks.py
from fastapi import APIRouter
from celery.result import AsyncResult
from tasks.jobs import long_running_task
from tasks.celery_app import celery_app

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/start/{n}")
def start_task(n: int):
    res = long_running_task.delay(n)
    return {"task_id": res.id, "status": res.status}

@router.get("/status/{task_id}")
def status_task(task_id: str):
    r: AsyncResult = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": r.status, "result": r.result if r.ready() else None}