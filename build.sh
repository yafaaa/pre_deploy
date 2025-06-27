#!/usr/bin/env bash
# Exit on error
set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

echo "Python version:"
python --version

echo "Pip version:"
pip --version

echo "Installing only critical dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Build completed."
