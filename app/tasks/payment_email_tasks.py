from celery import shared_task
from app.services.email_service import send_email
from app.services.email_templates import money, render_email
from app.core.logging_config import request_id_ctx
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name="notification.send_invoice_refunded_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
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
        body, html_body = render_email(
            eyebrow="Refund processed",
            title=f"Invoice #{invoice_id} was refunded",
            greeting_name=customer_name,
            intro="Your refund has been processed successfully.",
            details=[
                ("Invoice", f"#{invoice_id}"),
                ("Refunded amount", money(total)),
                ("Status", "REFUNDED"),
            ],
            text_extra="If you have any questions, please contact support.",
            html_extra='<p style="margin:18px 0 0;font-size:15px;line-height:1.6;color:#3f3f46;">If you have any questions, please contact support.</p>',
        )

        send_email(to_email=email, subject=subject, body=body, html_body=html_body)

        logger.info(
            "INVOICE_REFUNDED email sent",
            extra={"invoice_id": invoice_id, "email": email},
        )

    except Exception:
        logger.error("INVOICE_REFUNDED failed", exc_info=True)
        raise
