import time
import uuid

from fastapi import APIRouter
from redis import Redis
from rq import Queue
import pandas as pd
from task.models import TaskResponse, TaskSchema

router = APIRouter()

redis_conn = Redis(host='redis', port=6379, db=0)
q = Queue('my_queue', connection=redis_conn)


def create_task(task_type):
    name = f"/storage/{str(uuid.uuid4())}.csv"
    pd.DataFrame([{'a':1}]).to_csv(name)
    time.sleep(int(task_type) * 10)
    return True


@router.post("/", status_code=201)
async def run_task(payload: TaskSchema):
    task = q.enqueue(create_task, payload.task_type)
    response_object = {
        "status": "success",
        "task_id": task.get_id()
    }
    return response_object
