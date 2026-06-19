from celery import shared_task
from app.services.email_service import send_email
from app.services.email_templates import render_email
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name="notification.send_signup_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_signup_email(self, payload):

    logger.info(f"Received signup event: {payload}")

    try:
        data = payload["payload"]
        subject = "Welcome to Opslora"
        body, html_body = render_email(
            eyebrow="Account created",
            title="Welcome to Opslora",
            greeting_name=data.get("full_name") or data.get("email", "there"),
            intro=f"Your organization \"{data['organization_name']}\" has been created successfully.",
            details=[
                ("Organization", data["organization_name"]),
                ("Email", data["email"]),
            ],
            text_extra="You can now manage customers, orders, invoices, payments, and inventory in one place.",
            html_extra='<p style="margin:18px 0 0;font-size:15px;line-height:1.6;color:#3f3f46;">You can now manage customers, orders, invoices, payments, and inventory in one place.</p>',
        )

        send_email(
            to_email=data["email"],
            subject=subject,
            body=body,
            html_body=html_body,
        )

        logger.info(f"Signup email processed for user_id={data['user_id']}")

    except Exception as e:
        logger.error(f"Task failed for payload {payload}: {e}")
        raise
