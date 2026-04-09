from celery import shared_task
from app.services.email_service import send_email
from app.core.logging_config import request_id_ctx
import logging

logger = logging.getLogger(__name__)


# -----------------------------
# INVOICE CREATED
# -----------------------------
@shared_task(
    name="notification.send_invoice_created_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5}
)
def send_invoice_created_email(self, payload, request_id=None):

    request_id_ctx.set(request_id or "N/A")

    logger.info("Processing INVOICE_CREATED event", extra={"payload": payload})

    try:
        email = payload.get("email")
        customer_name = payload.get("customer_name", "Customer")
        invoice_id = payload.get("invoice_id")
        order_id = payload.get("order_id")
        total = payload.get("total")

        if not email:
            raise ValueError("Missing email")

        subject = f"Invoice #{invoice_id} Created"

        body = f"""
Hello {customer_name},

Your invoice #{invoice_id} has been generated.

🧾 Order ID: {order_id}
💰 Total: ₹{total}
📌 Status: UNPAID

Please complete payment before due date.

– Opslora Team
"""

        send_email(email, subject, body)

        logger.info("INVOICE_CREATED email sent", extra={"invoice_id": invoice_id})

    except Exception as e:
        logger.error("INVOICE_CREATED failed", exc_info=True)
        raise


# -----------------------------
# INVOICE PAID
# -----------------------------
@shared_task(
    name="notification.send_invoice_paid_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5}
)
def send_invoice_paid_email(self, payload, request_id=None):

    request_id_ctx.set(request_id or "N/A")

    logger.info("Processing INVOICE_PAID event", extra={"payload": payload})

    try:
        email = payload.get("email")
        customer_name = payload.get("customer_name", "Customer")
        invoice_id = payload.get("invoice_id")
        total = payload.get("total")

        subject = f"Invoice #{invoice_id} Paid"

        body = f"""
Hello {customer_name},

🎉 Your payment has been received.

Invoice #{invoice_id} is now PAID.

💰 Amount: ₹{total}

Thank you!

– Opslora Team
"""

        send_email(email, subject, body)

        logger.info("INVOICE_PAID email sent", extra={"invoice_id": invoice_id})

    except Exception as e:
        logger.error("INVOICE_PAID failed", exc_info=True)
        raise


# -----------------------------
# INVOICE CANCELLED
# -----------------------------
@shared_task(
    name="notification.send_invoice_cancelled_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5}
)
def send_invoice_cancelled_email(self, payload, request_id=None):

    request_id_ctx.set(request_id or "N/A")

    logger.info("Processing INVOICE_CANCELLED event", extra={"payload": payload})

    try:
        email = payload.get("email")
        customer_name = payload.get("customer_name", "Customer")
        invoice_id = payload.get("invoice_id")

        subject = f"Invoice #{invoice_id} Cancelled"

        body = f"""
Hello {customer_name},

Your invoice #{invoice_id} has been cancelled.

If this was unexpected, contact support.

– Opslora Team
"""

        send_email(email, subject, body)

        logger.info("INVOICE_CANCELLED email sent", extra={"invoice_id": invoice_id})

    except Exception as e:
        logger.error("INVOICE_CANCELLED failed", exc_info=True)
        raise