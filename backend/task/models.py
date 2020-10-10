from pydantic import BaseModel


class TaskSchema(BaseModel):
    task_type: int


class TaskResponse(TaskSchema):
    status: str
    task_id: str

