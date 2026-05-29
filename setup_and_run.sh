#!/bin/bash
# AutoElite Car Dealership — Ubuntu Setup Script
# Run this from the project root (where manage.py lives)

set -e
echo "============================================"
echo "  AutoElite Dealership — Setup Script"
echo "============================================"

# 1. Create & activate virtual environment
echo "[1/6] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "[2/6] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run migrations
echo "[3/6] Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# 4. Seed sample data
echo "[4/6] Seeding sample data..."
python manage.py seed_data

# 5. Collect static files
echo "[5/6] Collecting static files..."
python manage.py collectstatic --noinput

# 6. Create superuser (interactive)
echo "[6/6] Creating admin superuser..."
python manage.py createsuperuser

echo ""
echo "============================================"
echo "  Setup complete! Starting server..."
echo "  Visit: http://127.0.0.1:8000"
echo "  Admin: http://127.0.0.1:8000/admin"
echo "============================================"
python manage.py runserver
