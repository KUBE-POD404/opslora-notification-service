import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

logger = logging.getLogger(__name__)


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "Opslora")


def send_email(to_email: str, subject: str, body: str):

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    try:
        logger.info(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT}")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()

            if SMTP_USER and SMTP_PASS:
                server.login(SMTP_USER, SMTP_PASS)

            server.send_message(msg)

        logger.info(f"Email successfully sent to {to_email}")

    except Exception as e:
        logger.error(f"Email sending failed to {to_email}: {e}")
        raise