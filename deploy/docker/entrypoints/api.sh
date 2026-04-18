#!/bin/sh

set -e

echo "Waiting for database..."

# optional wait loop (simple)
while ! nc -z db 5432; do
  sleep 1
done

echo "Database ready!"

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000