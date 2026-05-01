#!/bin/sh
set -e

python - <<'PY'
import socket
import time

host = "rabbitmq"
port = 5672

for attempt in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"RabbitMQ is ready at {host}:{port}")
            break
    except OSError:
        print(f"Waiting for RabbitMQ at {host}:{port}...")
        time.sleep(2)
else:
    raise SystemExit("RabbitMQ did not become ready")
PY

exec celery -A app.core.celery_app worker --loglevel=info -Q notification_queue -n notification@%h --concurrency=2
