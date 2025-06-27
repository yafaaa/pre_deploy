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
pip install --no-cache-dir gunicorn

echo "Build completed."
