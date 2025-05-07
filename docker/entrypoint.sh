#!/bin/sh

echo "Waiting for PostgreSQL..."

until pg_isready -U $POSTGRES_USER -d $POSTGRES_DB -h db; do
  sleep 1
done

echo "PostgreSQL started"

cd /app

echo "Starting FastAPI..."
exec $POETRY_HOME/bin/poetry run fastapi run songs_api/main.py
