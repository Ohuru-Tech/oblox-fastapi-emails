from pydantic import BaseModel, ConfigDict


class TaskExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    task_name: str
    task_id: int
    secret_key: str
