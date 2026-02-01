from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_emails.models.task import Task, TaskStatus


class TasksRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_task(self, task: Task) -> Task:
        async with self._db.begin() as session:
            session.add(task)
        return task

    async def get_task_by_id(self, id: int) -> Task:
        result = await self._db.execute(select(Task).where(Task.id == id))
        return result.scalar_one_or_none()

    async def update_task_result(
        self,
        task_id: int,
        result: str | None = None,
        error: str | None = None,
        traceback: str | None = None,
    ) -> Task:
        task = await self.get_task_by_id(task_id)
        if result:
            task.result = result
        if error:
            task.error = error
        if traceback:
            task.traceback = traceback
        task.status = TaskStatus.COMPLETED if result else TaskStatus.FAILED
        await self._db.commit()
        return task
