#!/usr/bin/env bash
# Exit on error
set -o errexit

# Print each command before executing it
set -o xtrace

echo "Installing Python dependencies..."
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies with --no-cache-dir to save memory
python -m pip install --no-cache-dir -r requirements.txt

echo "Running collectstatic..."
python manage.py collectstatic --no-input --clear

echo "Running migrations..."
python manage.py migrate --noinput

echo "Build script completed successfully!"
