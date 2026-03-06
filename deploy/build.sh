#!/usr/bin/env bash
# Exit on error
set -o errexit

echo ">>> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

echo ">>> Running migrations..."
python manage.py migrate

echo ">>> Collecting static files..."
python manage.py collectstatic --no-input

# Optional: Seed the database
# echo ">>> Seeding database..."
# python database/seed.py
