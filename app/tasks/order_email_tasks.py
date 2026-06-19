from celery import shared_task
from app.services.email_service import send_email
from app.services.email_templates import order_items_html, order_items_text, render_email
import logging

logger = logging.getLogger(__name__)


def format_order_items(items: list) -> str:
    return order_items_text(items)


def _send_order_email(payload, *, event_name: str, subject: str, title: str, intro: str, status: str, text_extra: str):
    data = payload["payload"]
    email = data.get("email")
    customer_name = data.get("customer_name", "Customer")
    order_id = data.get("order_id")
    items = data.get("items", [])

    if not email:
        raise ValueError("Missing email in payload")

    body, html_body = render_email(
        eyebrow=event_name,
        title=title,
        greeting_name=customer_name,
        intro=intro,
        details=[("Order", f"#{order_id}"), ("Status", status)],
        text_extra=f"Order details:\n{order_items_text(items)}\n\n{text_extra}",
        html_extra=(
            '<div style="margin-top:18px;">'
            '<div style="color:#71717a;font-size:13px;margin-bottom:8px;">Order details</div>'
            f"{order_items_html(items)}"
            f'<p style="margin:18px 0 0;font-size:15px;line-height:1.6;color:#3f3f46;">{text_extra}</p>'
            "</div>"
        ),
    )

    send_email(to_email=email, subject=subject, body=body, html_body=html_body)
    logger.info(f"{event_name} email sent", extra={"order_id": order_id, "email": email})


@shared_task(
    name="notification.send_order_created_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_order_created_email(self, payload):

    logger.info("Processing ORDER_CREATED event", extra={"payload": payload})

    try:
        order_id = payload["payload"].get("order_id")
        _send_order_email(
            payload,
            event_name="Order created",
            subject=f"Order #{order_id} Created",
            title=f"Order #{order_id} was created",
            intro="Your order has been created successfully.",
            status="CREATED",
            text_extra="We will notify you once your order is confirmed.",
        )

    except Exception as e:
        logger.error(f"ORDER_CREATED task failed: {e}", extra={"payload": payload})
        raise


@shared_task(
    name="notification.send_order_confirmed_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_order_confirmed_email(self, payload):

    logger.info("Processing ORDER_CONFIRMED event", extra={"payload": payload})

    try:
        order_id = payload["payload"].get("order_id")
        _send_order_email(
            payload,
            event_name="Order confirmed",
            subject=f"Order #{order_id} Confirmed",
            title=f"Order #{order_id} is confirmed",
            intro="Your order has been confirmed.",
            status="CONFIRMED",
            text_extra="Thank you for choosing Opslora.",
        )

    except Exception as e:
        logger.error(f"ORDER_CONFIRMED task failed: {e}", extra={"payload": payload})
        raise


@shared_task(
    name="notification.send_order_cancelled_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_order_cancelled_email(self, payload):

    logger.info("Processing ORDER_CANCELLED event", extra={"payload": payload})

    try:
        order_id = payload["payload"].get("order_id")
        _send_order_email(
            payload,
            event_name="Order cancelled",
            subject=f"Order #{order_id} Cancelled",
            title=f"Order #{order_id} was cancelled",
            intro="Your order has been cancelled.",
            status="CANCELLED",
            text_extra="If this was unexpected, please contact support.",
        )

    except Exception as e:
        logger.error(f"ORDER_CANCELLED task failed: {e}", extra={"payload": payload})
        raise
