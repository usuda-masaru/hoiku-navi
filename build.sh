#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify gunicorn installation
echo "=== Checking gunicorn installation ==="
which gunicorn || echo "gunicorn not in PATH"
pip show gunicorn

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

echo "=== Build complete ==="