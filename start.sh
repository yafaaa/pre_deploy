#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
gunicorn project4.wsgi:application --bind 0.0.0.0:$PORT
