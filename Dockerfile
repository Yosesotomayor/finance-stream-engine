# =======
# Builder
# =======

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

# =======
# Runner
# =======

FROM python:3.12-slim-bookworm AS runner

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/

RUN chown -R appuser:appuser /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app

USER appuser