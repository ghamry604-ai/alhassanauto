#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e

echo "=========================================="
echo "  Starting Production Server (Railway)"
echo "=========================================="

# 1. Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# 2. Check if a seed argument or flag is set, or if we want to run any other startup tasks
# (Optional: e.g. python manage.py seed_data)

# 3. Start Gunicorn application server
echo "Starting Gunicorn..."
exec gunicorn carsite.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 3 --threads 2 --log-file -
