import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, body: str):

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = f"{settings.from_name} <{settings.from_email}>"
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    try:
        logger.info(f"Connecting to SMTP server {settings.smtp_host}:{settings.smtp_port}")

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_starttls:
                server.starttls()

            if settings.smtp_user and settings.smtp_pass:
                server.login(settings.smtp_user, settings.smtp_pass)

            server.send_message(msg)

        logger.info(f"Email successfully sent to {to_email}")

    except Exception as e:
        logger.error(f"Email sending failed to {to_email}: {e}")
        raise
