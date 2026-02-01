from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_emails.database import get_database_session
from fastapi_emails.models.templates import Template


class TemplatesRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_template_by_name(self, name: str) -> Template:
        result = await self._db.execute(select(Template).where(Template.name == name))
        template = result.scalar_one_or_none()
        if not template:
            raise ValueError(f"Template {name} not found")
        return template


def get_templates_repository(
    database_session: AsyncSession = Depends(get_database_session),
) -> TemplatesRepository:
    return TemplatesRepository(database_session)
