#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Vercel Build Phase Started ==="

# 1. Install dependencies
echo "Installing requirements..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 2. Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "=== Vercel Build Phase Finished ==="
