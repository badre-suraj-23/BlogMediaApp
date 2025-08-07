#!/bin/bash

# Stop on errors
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (for production)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate