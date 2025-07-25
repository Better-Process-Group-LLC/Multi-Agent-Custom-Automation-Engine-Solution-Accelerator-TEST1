
# Base Python image
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye AS base
WORKDIR /app

FROM base AS builder
# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app
# Copy only backend dependencies
COPY uv.lock pyproject.toml /app/

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy backend source only (avoid frontend and other files)
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

FROM base

WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /bin/uv /bin/uv

ENV PATH="/app/.venv/bin:$PATH"

# Ensure main.py exists at /app/main.py
# If your main.py is in src/backend, copy it explicitly
COPY src/backend/main.py /app/main.py

EXPOSE 8000
ENV WEBSITES_PORT=8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
