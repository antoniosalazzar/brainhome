#!/bin/sh
set -e

echo "Waiting for Postgres..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Postgres is up"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting API"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
