#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

echo "Current directory:"
pwd

echo "Directory contents:"
ls -la

echo "Installing remaining dependencies..."
pip install --no-cache-dir -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || {
    echo "Collectstatic failed but continuing..."
}

echo "Running migrations..."
python manage.py migrate --noinput || {
    echo "Migration failed but continuing..."
}

echo "Starting Gunicorn..."
exec gunicorn project4.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 2
