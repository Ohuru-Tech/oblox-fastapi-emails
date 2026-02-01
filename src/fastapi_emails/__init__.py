"""
FastAPI Emails - Email sending module for FastAPI applications.

Provides email templates, multiple providers, and async task queuing.
"""

# Configuration
from fastapi_emails.settings.config import (
    EmailConfigModel,
    configure_settings,
    get_settings,
)

# Email Service
from fastapi_emails.services.emails import EmailService, get_email_service

# Task/Queue functionality
from fastapi_emails.tasks.emails import send_email_now

# Router for Google Cloud Tasks
from fastapi_emails.routers.v1.gcloud_task_executor_router import (
    gcloud_task_executor_router,
)

# Models
from fastapi_emails.models.templates import Template

# Repositories
from fastapi_emails.repositories.templates import (
    TemplatesRepository,
    get_templates_repository,
)

# Database
from fastapi_emails.database import create_tables

__all__ = [
    # Configuration
    "EmailConfigModel",
    "configure_settings",
    "get_settings",
    # Email Service
    "EmailService",
    "get_email_service",
    # Task/Queue
    "send_email_now",
    # Router
    "gcloud_task_executor_router",
    # Models
    "Template",
    # Repositories
    "TemplatesRepository",
    "get_templates_repository",
    # Database
    "create_tables",
]
