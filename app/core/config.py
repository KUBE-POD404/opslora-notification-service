import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _load_environment_file() -> None:
    """Load the correct dotenv file for local development only.

    Runtime platforms inject env directly:
    - Docker Compose passes environment/env_file values.
    - AKS receives values from Kubernetes Secrets generated from Key Vault.
    - EC2/systemd can pass values from its own environment.

    ENV_FILE is an explicit override. Otherwise ENVIRONMENT selects .env.<env>
    before falling back to .env.
    """
    env_file = os.getenv("ENV_FILE")
    if env_file:
        load_dotenv(env_file)
        return

    environment = os.getenv("ENVIRONMENT", "development")
    candidate = Path(f".env.{environment}")
    if candidate.exists():
        load_dotenv(candidate)
        return

    load_dotenv()


_load_environment_file()


def _secret(name: str, default: str | None = None, *, required: bool = False) -> str:
    """Read a config value from NAME or NAME_FILE.

    NAME_FILE supports Docker/Kubernetes mounted secrets, including Azure Key
    Vault CSI Driver volumes. Environment variables continue to work for local
    Docker and CI, so the application code does not depend on Azure SDKs.
    """
    file_name = os.getenv(f"{name}_FILE")
    if file_name:
        value = Path(file_name).read_text(encoding="utf-8").strip()
    else:
        value = os.getenv(name, default)

    if required and not value:
        raise RuntimeError(f"{name} is not set")

    return value or ""


def _int(name: str, default: int) -> int:
    return int(_secret(name, str(default)))


def _bool(name: str, default: bool = False) -> bool:
    value = _secret(name)
    if not value:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    service_name: str = _secret("SERVICE_NAME", "notification-service")
    environment: str = _secret("ENVIRONMENT", "development")
    log_level: str = _secret("LOG_LEVEL", "INFO")
    rabbitmq_url: str = _secret("RABBITMQ_URL", required=True)
    smtp_host: str = _secret("SMTP_HOST", required=True)
    smtp_port: int = _int("SMTP_PORT", 587)
    smtp_user: str = _secret("SMTP_USER", "")
    smtp_pass: str = _secret("SMTP_PASS", "")
    smtp_starttls: bool = _bool("SMTP_STARTTLS", True)
    from_email: str = _secret("FROM_EMAIL", required=True)
    from_name: str = _secret("FROM_NAME", "Opslora")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
