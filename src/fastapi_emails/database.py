from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_emails.models.base import Base
# Import models to register them with Base.metadata
from fastapi_emails.models.task import Task  # noqa: F401
from fastapi_emails.models.templates import Template  # noqa: F401
from fastapi_emails.settings.config import get_settings
from fastapi_emails.utils.logging import get_logger

settings = get_settings()
logger = get_logger("database")

engine = create_async_engine(settings.databse_url, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    """
    Create all database tables defined in the models.
    
    This function creates the following tables:
    - templates: Stores email templates
    - tasks: Stores task execution records
    
    Example:
        await create_tables()
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


async def get_database_session():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(e)
