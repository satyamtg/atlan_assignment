from time import sleep

from celery.result import AsyncResult

from .celery_app import celery_app


def iterative_task(iter_delay, iteration):
    sleep(iter_delay)
    return iteration + 1


@celery_app.task(acks_late=True, bind=True)
def test_celery(self, iter_delay: int) -> str:
    self.update_state(state="PROCESSING")
    for i in range(1, 101):
        task = AsyncResult(self.request.id)
        while task.state == "PAUSE":
            sleep(1)
            if task.state == "RESUME":
                self.update_state(state="PROCESSING")
        i = iterative_task(iter_delay, i - 1)
        curr_state = AsyncResult(self.request.id).state
        self.update_state(state=curr_state, meta={"progress_percent": i})
    return f"Task {self.request.id} completed successfully"
