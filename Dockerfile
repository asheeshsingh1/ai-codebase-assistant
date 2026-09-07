FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# System dependencies required for git operations and Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Install dependency files first so Docker can cache this layer
COPY pyproject.toml poetry.lock* ./

RUN poetry install --only main --no-root

# Copy application
COPY app ./app
COPY alembic.ini ./
COPY alembic ./alembic

# Directory where repositories will be cloned
RUN mkdir -p /repositories

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]