from celery import Celery
import app.core.celery_signals
from app.core.config import settings

RABBITMQ_URL = settings.rabbitmq_url

celery = Celery(
    "notification_service",
    broker=RABBITMQ_URL,
    backend="rpc://"
)

celery.conf.update(
    imports=[
        "app.tasks.email_tasks",
        "app.tasks.order_email_tasks",
        "app.tasks.invoice_email_tasks",
        "app.tasks.payment_email_tasks",
    ],
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

