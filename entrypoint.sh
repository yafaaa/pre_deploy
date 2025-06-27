#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn project4.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --timeout 120
