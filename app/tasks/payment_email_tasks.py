from celery import shared_task
from app.services.email_service import send_email
from app.core.logging_config import request_id_ctx
import logging

logger = logging.getLogger(__name__)


# -----------------------------
# INVOICE REFUNDED
# -----------------------------
@shared_task(
    name="notification.send_invoice_refunded_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5}
)
def send_invoice_refunded_email(self, payload, request_id=None):

    request_id_ctx.set(request_id or "N/A")

    logger.info("Processing INVOICE_REFUNDED event", extra={"payload": payload})

    try:
        email = payload.get("email")
        customer_name = payload.get("customer_name", "Customer")
        invoice_id = payload.get("invoice_id")
        total = payload.get("total")

        if not email:
            raise ValueError("Missing email in payload")

        subject = f"Invoice #{invoice_id} Refunded"

        body = f"""
Hello {customer_name},

Your refund has been processed successfully.

🧾 Invoice ID: {invoice_id}
💰 Refunded Amount: ₹{total}

If you have any questions, feel free to contact support.

– Opslora Team
"""

        send_email(
            to_email=email,
            subject=subject,
            body=body
        )

        logger.info(
            "INVOICE_REFUNDED email sent",
            extra={"invoice_id": invoice_id, "email": email}
        )

    except Exception as e:
        logger.error("INVOICE_REFUNDED failed", exc_info=True)
        raise