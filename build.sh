#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies  
python -m pip install -r requirements.txt

# Verify gunicorn installation
echo "=== Checking gunicorn installation ==="
python -m pip show gunicorn
python -c "import gunicorn; print(f'Gunicorn version: {gunicorn.__version__}')"

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

echo "=== Build complete ==="#