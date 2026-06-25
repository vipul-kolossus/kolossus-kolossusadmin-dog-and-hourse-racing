#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py seed_data 2>/dev/null || true
exec gunicorn racing_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
