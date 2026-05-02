from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/notification", tags=["health"])


@router.get("/health")
@router.get("/live")
def live():
    return {"status": "ok"}


@router.get("/startup")
def startup():
    return live()


@router.get("/ready")
def ready():
    checks = {
        "rabbitmq_config": "ok" if settings.rabbitmq_url else "error",
        "smtp_config": "ok" if settings.smtp_host and settings.from_email else "error",
    }
    status = "ready" if all(value == "ok" for value in checks.values()) else "not_ready"
    return {"status": status, "checks": checks}
