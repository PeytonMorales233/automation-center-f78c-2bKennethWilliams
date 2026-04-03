FROM python:3.11-slim-bookworm AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and poetry.lock (or requirements.txt) first for layer caching
COPY pyproject.toml .
COPY requirements.txt .

# Install Python build dependencies and pip-tools (lightweight, no Poetry bloat)
FROM base AS builder
RUN pip install --no-cache-dir pip-tools

# Compile requirements if needed (e.g., via pip-compile), but here we use plain requirements.txt
# For simplicity & CI/CD clarity, skip compilation — rely on pinned requirements.txt

# Install production dependencies only
RUN pip install --no-cache-dir --user -r requirements.txt


FROM base AS runtime

# Create non-root user
RUN addgroup -g 1001 -f appgroup && adduser -S appuser -u 1001

# Copy installed dependencies from builder stage
COPY --from=builder --chown=appuser:appgroup /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Healthcheck (lightweight, avoids external deps)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run with uvicorn, production-ready flags
CMD ["uvicorn", "main:app", "--host=0.0.0.0:8000", "--port=8000", "--workers=2", "--log-level=info", "--proxy-headers", "--forwarded-allow-ips=*"]