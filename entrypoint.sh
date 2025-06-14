#!/bin/bash
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting server..."
exec python3 run.py
