import os


os.environ.setdefault("RABBITMQ_URL", "memory://")
os.environ.setdefault("SMTP_HOST", "localhost")
os.environ.setdefault("SMTP_PORT", "1025")
os.environ.setdefault("SMTP_USER", "")
os.environ.setdefault("SMTP_PASS", "")
os.environ.setdefault("SMTP_STARTTLS", "false")
os.environ.setdefault("FROM_EMAIL", "noreply@example.com")
os.environ.setdefault("FROM_NAME", "Opslora")
