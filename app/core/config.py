import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "notification-service")
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    rabbitmq_url: str = _required("RABBITMQ_URL")
    smtp_host: str = _required("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_pass: str = os.getenv("SMTP_PASS", "")
    smtp_starttls: bool = _bool("SMTP_STARTTLS", True)
    from_email: str = _required("FROM_EMAIL")
    from_name: str = os.getenv("FROM_NAME", "Opslora")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
