from celery import shared_task
from app.services.email_service import send_email
from app.services.email_templates import money, render_email
from app.core.logging_config import request_id_ctx
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name="notification.send_invoice_created_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
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
        body, html_body = render_email(
            eyebrow="Invoice created",
            title=f"Invoice #{invoice_id} is ready",
            greeting_name=customer_name,
            intro="Your invoice has been generated and is currently unpaid.",
            details=[
                ("Invoice", f"#{invoice_id}"),
                ("Order", f"#{order_id}"),
                ("Total", money(total)),
                ("Status", "UNPAID"),
            ],
            text_extra="Please complete payment before the due date.",
            html_extra='<p style="margin:18px 0 0;font-size:15px;line-height:1.6;color:#3f3f46;">Please complete payment before the due date.</p>',
        )

        send_email(email, subject, body, html_body=html_body)
        logger.info("INVOICE_CREATED email sent", extra={"invoice_id": invoice_id})

    except Exception:
        logger.error("INVOICE_CREATED failed", exc_info=True)
        raise


@shared_task(
    name="notification.send_invoice_paid_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_invoice_paid_email(self, payload, request_id=None):

    request_id_ctx.set(request_id or "N/A")
    logger.info("Processing INVOICE_PAID event", extra={"payload": payload})

    try:
        email = payload.get("email")
        customer_name = payload.get("customer_name", "Customer")
        invoice_id = payload.get("invoice_id")
        total = payload.get("total")

        if not email:
            raise ValueError("Missing email")

        subject = f"Invoice #{invoice_id} Paid"
        body, html_body = render_email(
            eyebrow="Payment received",
            title=f"Invoice #{invoice_id} is paid",
            greeting_name=customer_name,
            intro="We have received the payment for this invoice.",
            details=[
                ("Invoice", f"#{invoice_id}"),
                ("Amount", money(total)),
                ("Status", "PAID"),
            ],
            text_extra="Thank you for your payment.",
            html_extra='<p style="margin:18px 0 0;font-size:15px;line-height:1.6;color:#3f3f46;">Thank you for your payment.</p>',
        )

        send_email(email, subject, body, html_body=html_body)
        logger.info("INVOICE_PAID email sent", extra={"invoice_id": invoice_id})

    except Exception:
        logger.error("INVOICE_PAID failed", exc_info=True)
        raise


@shared_task(
    name="notification.send_invoice_cancelled_email",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_invoice_cancelled_email(self, payload, request_id=None):

    request_id_ctx.set(request_id or "N/A")
    logger.info("Processing INVOICE_CANCELLED event", extra={"payload": payload})

    try:
        email = payload.get("email")
        customer_name = payload.get("customer_name", "Customer")
        invoice_id = payload.get("invoice_id")

        if not email:
            raise ValueError("Missing email")

        subject = f"Invoice #{invoice_id} Cancelled"
        body, html_body = render_email(
            eyebrow="Invoice cancelled",
            title=f"Invoice #{invoice_id} was cancelled",
            greeting_name=customer_name,
            intro="This invoice has been cancelled.",
            details=[("Invoice", f"#{invoice_id}"), ("Status", "CANCELLED")],
            text_extra="If this was unexpected, please contact support.",
            html_extra='<p style="margin:18px 0 0;font-size:15px;line-height:1.6;color:#3f3f46;">If this was unexpected, please contact support.</p>',
        )

        send_email(email, subject, body, html_body=html_body)
        logger.info("INVOICE_CANCELLED email sent", extra={"invoice_id": invoice_id})

    except Exception:
        logger.error("INVOICE_CANCELLED failed", exc_info=True)
        raise
