#!/bin/sh

set -eu

MAX_ATTEMPTS=30
ATTEMPT=0

echo "Waiting for PostgreSQL at ${DJANGO_DB_HOST:-<missing>}:${DJANGO_DB_PORT:-<missing>}..."

while ! nc -z "${DJANGO_DB_HOST:-}" "${DJANGO_DB_PORT:-5432}"; do
  ATTEMPT=$((ATTEMPT + 1))

  if [ "$ATTEMPT" -ge "$MAX_ATTEMPTS" ]; then
    echo "Could not connect to PostgreSQL after ${MAX_ATTEMPTS} attempts."
    exit 1
  fi

  echo "PostgreSQL not reachable yet, retry ${ATTEMPT}/${MAX_ATTEMPTS}..."
  sleep 2
done

echo "PostgreSQL is up - running migrations and collectstatic..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn --bind 0.0.0.0:8000 ai_powered_blog.wsgi:application
