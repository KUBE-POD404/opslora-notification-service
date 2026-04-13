FROM dhi.io/python:3.13-dev AS builder
 
WORKDIR /app
 
ENV PATH="/app/venv/bin:$PATH"
 
RUN python -m venv /app/venv
 
COPY requirements.txt .

# Install dependencies inside virtual environment using cached pip downloads 
RUN --mount=type=cache,target=/root/.cache/pip \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt
 
FROM dhi.io/python:3.13
 
WORKDIR /app
 
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
 
 
COPY --from=builder --chown=0:0 --chmod=0555 /app/venv /app/venv
COPY --chown=0:0 --chmod=0555 app/ ./app/
 
USER 10001
 
 
CMD ["celery", "-A", "app.core.celery_app", "worker",
     "--loglevel=info",
     "-Q", "notification_queue",
     "-n", "notification@%h",
     "--concurrency=2"]
 