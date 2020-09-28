import logging
from celery.result import AsyncResult
from celery.task.control import revoke
from celery.app.task import Task
from fastapi import BackgroundTasks, FastAPI

from worker.celery_worker import test_celery
from worker.celery_app import celery_app

log = logging.getLogger(__name__)

app = FastAPI()


def celery_on_message(body):
    log.warn(body)


def background_on_message(task):
    log.warn(task.get(on_message=celery_on_message, propagate=False))


@app.get("/start/{iter_delay}")
async def root(iter_delay: int, background_task: BackgroundTasks):
    task = celery_app.send_task(
        "app.worker.celery_worker.test_celery", args=[iter_delay]
    )
    background_task.add_task(background_on_message, task)
    return {"message": "task started", "task_id": task.id}


@app.get("/cancel/{task_id}")
async def cancel(task_id: str):
    revoke(task_id, terminate=True)
    return {"message": "task terminated"}


@app.get("/pause/{task_id}")
async def pause(task_id: str, background_task: BackgroundTasks):
    if AsyncResult(task_id).status == "PAUSE":
        background_task.add_task(background_on_message, AsyncResult(task_id))
        return {"message": "already paused"}
    Task.update_state(self=test_celery, task_id=task_id, state="PAUSE")
    task = None
    while True:
        task = AsyncResult(task_id)
        if task.status == "PAUSE":
            break
    background_task.add_task(background_on_message, task)
    return {"message": "task paused"}


@app.get("/resume/{task_id}")
async def resume(task_id: str, background_task: BackgroundTasks):
    if AsyncResult(task_id).status != "PAUSE":
        background_task.add_task(background_on_message, AsyncResult(task_id))
        return {"message": "task already runing"}
    Task.update_state(self=test_celery, task_id=task_id, state="RESUME")
    task = None
    while True:
        task = AsyncResult(task_id)
        if task.status != "PAUSE":
            break
    background_task.add_task(background_on_message, task)
    return {"message": "task resumed"}
