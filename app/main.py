from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.middleware import RequestContextMiddleware

setup_logging()

if settings.is_production:
    docs_url = None
    redoc_url = None
    openapi_url = None
else:
    docs_url = "/notification/docs"
    redoc_url = "/notification/redoc"
    openapi_url = "/notification/openapi.json"

app = FastAPI(
    title="Notification Service",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

app.add_middleware(RequestContextMiddleware)


@app.get("/api/v1/notification/health")
def health():
    return {"status": "ok"}


@app.get("/api/notification/health", include_in_schema=False)
def legacy_health():
    return health()
