#!/bin/sh

set -e

echo "Waiting for PostgreSQL at $DJANGO_DB_HOST:$DJANGO_DB_PORT..."

while ! nc -z "$DJANGO_DB_HOST" "$DJANGO_DB_PORT"; do
  sleep 1
done

echo "PostgreSQL is up - running migrations and collectstatic..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn --bind 0.0.0.0:8000 ai_powered_blog.wsgi:application
