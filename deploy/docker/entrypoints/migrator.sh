#!/bin/sh
set -e

echo "Running database migrations..."

cd /usr/src/app/src/backend

alembic upgrade head

echo "Migrations completed."