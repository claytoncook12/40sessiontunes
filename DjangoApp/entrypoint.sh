#!/bin/sh

# Make Migrations to Database
python manage.py migrate --noinput

# Collect Static
python manage.py collectstatic --noinput

# CreateSuperUser
# python manage.py createsuperuser --noinput

# Start Server
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 5