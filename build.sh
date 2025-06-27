#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Build script completed successfully!"
