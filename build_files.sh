#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Vercel Build Phase Started ==="

# 1. Create a temporary virtual environment to bypass PEP 668 (externally-managed-environment)
echo "Creating temporary virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies inside the virtual environment
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

# 4. Deactivate virtual environment
deactivate

echo "=== Vercel Build Phase Finished ==="
