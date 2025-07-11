#!/bin/sh

echo "🚦 Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Running Alembic migrations..."
alembic upgrade head

echo "🌱 Seeding initial data..."
python app/seed_data.py

echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
