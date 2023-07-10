#!/usr/bin/env bash
# exit on error
set -o errexit


python -m pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
# The default password for the initial superuser comes from env variable DJANGO_SUPERUSER_PASSWORD
python manage.py createsuperuser --no-input --username meenkari --email meenkari@meenkari.com || { echo "default superuser already exists"; }
