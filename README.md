# FastAPI Emails

A FastAPI module for sending emails with support for templates, multiple providers, and async task queuing.

## Features

- **Email Templates**: Store and render email templates using Jinja2
- **Multiple Providers**: Support for Console (development), Mailgun, and Azure (planned)
- **Task Queuing**: Queue emails for async processing using Google Cloud Tasks or Taskiq
- **Direct Sending**: Send emails immediately without queuing

## Installation

```bash
pip install fastapi-emails
```

## Quick Start

```python
from fastapi import FastAPI, Depends
from fastapi_emails import (
    EmailConfigModel,
    EmailService,
    configure_settings,
    get_email_service,
)

# Configure settings (call this at app startup)
configure_settings(EmailConfigModel(
    provider="console"  # Use console for development
))

app = FastAPI()

# Send an email directly
@app.post("/send-email")
async def send_email(
    email_service: EmailService = Depends(get_email_service)
):
    await email_service.send_email(
        template_name="welcome",
        to="user@example.com",
        user_name="John"
    )
```

## Email Templates

Templates are stored in your database and use Jinja2 for rendering. Each template has:

- `name`: Unique identifier for the template
- `subject`: Email subject line (supports Jinja2 variables)
- `html_content`: HTML email body (optional)
- `text_content`: Plain text email body (required)

### Creating Templates

Templates are stored in the `templates` table. Create them via your database:

```python
from fastapi_emails import Template
from sqlalchemy.ext.asyncio import AsyncSession

async def create_template(db: AsyncSession):
    template = Template(
        name="welcome",
        subject="Welcome {{ user_name }}!",
        html_content="""
        <h1>Welcome {{ user_name }}!</h1>
        <p>Thanks for joining us.</p>
        """,
        text_content="Welcome {{ user_name }}! Thanks for joining us."
    )
    db.add(template)
    await db.commit()
```

### Template Variables

Pass variables to templates via `**kwargs` when sending:

```python
await email_service.send_email(
    template_name="welcome",
    to="user@example.com",
    user_name="John",
    company="Acme Corp"
)
```

These variables are available in your Jinja2 templates as `{{ user_name }}`, `{{ company }}`, etc.

## Sending Emails Directly

Use `EmailService` to send emails immediately without queuing:

```python
from fastapi import Depends
from fastapi_emails import EmailService, get_email_service

@app.post("/send-email")
async def send_email(
    email_service: EmailService = Depends(get_email_service)
):
    await email_service.send_email(
        template_name="notification",
        to="user@example.com",
        message="Your order has been shipped"
    )
```

The `send_email` method:

- Renders the template with provided variables
- Sends via the configured provider (Console, Mailgun, etc.)
- Returns immediately after sending

## Queuing Emails

Queue emails for async processing using task backends:

```python
from fastapi_emails import send_email_now

# Queue an email for async processing
await send_email_now(
    template_name="welcome",
    to="user@example.com",
    user_name="John"
)
```

### Google Cloud Tasks

For Google Cloud Tasks backend, register the executor router with your FastAPI app:

```python
from fastapi import FastAPI
from fastapi_emails import gcloud_task_executor_router

app = FastAPI()
app.include_router(gcloud_task_executor_router)
```

Configure settings:

```python
from fastapi_emails import EmailConfigModel, configure_settings

configure_settings(EmailConfigModel(
    provider="mailgun",
    task_system="google-cloud-tasks",
    task_secret_key="your-secret-key",
    gcloud_tasks_project="your-project",
    gcloud_tasks_location="us-central1",
    gcloud_tasks_queue="email-queue",
    handler_base="https://your-app.com",
    mailgun_api_key="your-api-key",
    mailgun_domain="your-domain.com"
))
```

## Configuration

Configure the module using `EmailConfigModel`:

```python
from fastapi_emails import EmailConfigModel, configure_settings

configure_settings(EmailConfigModel(
    # Provider selection
    provider="mailgun",  # Options: "console", "mailgun", "azure"
    
    # Task system
    task_system="google-cloud-tasks",  # Options: "taskiq", "google-cloud-tasks"
    
    # Mailgun settings (required if using mailgun provider)
    mailgun_api_key="your-api-key",
    mailgun_domain="your-domain.com",
    
    # Google Cloud Tasks settings (required if using google-cloud-tasks)
    task_secret_key="your-secret-key",
    gcloud_tasks_project="your-project",
    gcloud_tasks_location="us-central1",
    gcloud_tasks_queue="email-queue",
    handler_base="https://your-app.com",
    
    # Timezone
    timezone="UTC"
))
```

### Providers

#### Console Provider (Development)

Default provider for development. Logs emails to console instead of sending:

```python
from fastapi_emails import EmailConfigModel, configure_settings

configure_settings(EmailConfigModel(
    provider="console"
))
```

#### Mailgun Provider

For production email sending via Mailgun:

```python
from fastapi_emails import EmailConfigModel, configure_settings

configure_settings(EmailConfigModel(
    provider="mailgun",
    mailgun_api_key="your-api-key",
    mailgun_domain="your-domain.com"
))
```

#### Azure Provider

Azure provider is planned for future releases.

## Database Setup

The module requires a database with the following tables:

- `templates`: Stores email templates
- `tasks`: Stores task execution records (for queued emails)

### Creating Tables

You can create all required tables using the `create_tables()` function:

```python
from fastapi_emails import create_tables

# Create all tables
await create_tables()
```

Alternatively, you can run your database migrations to create these tables using SQLAlchemy. The database connection is configured separately in your application (the module uses `get_database_session()` for database access).
