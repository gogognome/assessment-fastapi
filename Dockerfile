FROM python:3.12.10-slim-bookworm AS build-phase

ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry==2.0.0

# Install dependencies to install psycopg2-binary and install postgresql-client-15, which is needed to check if PostgreSQL is running.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client-15 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

COPY docker/entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY pyproject.toml poetry.lock ./
RUN $POETRY_HOME/bin/poetry install --no-root

COPY songs_api/ songs_api/

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["./entrypoint.sh"]
