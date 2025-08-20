#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Verify gunicorn is installed
echo "Checking for gunicorn..."
pip list | grep gunicorn || echo "gunicorn not found in pip list"
which gunicorn || echo "gunicorn command not found"

python manage.py collectstatic --no-input
python manage.py migrate