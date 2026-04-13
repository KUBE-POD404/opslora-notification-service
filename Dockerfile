# ----------- BUILDER STAGE -----------
FROM dhi.io/python:3.13-dev AS builder

WORKDIR /app

# Create virtual environment
ENV PATH="/app/venv/bin:$PATH"
RUN python -m venv /app/venv

# Copy dependencies
COPY requirements.txt .

# Install dependencies with cache
RUN --mount=type=cache,target=/root/.cache/pip \
    /app/venv/bin/pip install -r requirements.txt


# ----------- RUNNER STAGE -----------
FROM dhi.io/python:3.13.13

WORKDIR /app

# Set environment variables
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy virtual environment from builder
COPY --from=builder --chown=0:0 --chmod=0555 /app/venv /app/venv

# Copy application code
COPY --chown=0:0 --chmod=0555 app/ ./app/

# Use non-root user
USER 10001

EXPOSE 3000

# Run application directly (no entrypoint)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]