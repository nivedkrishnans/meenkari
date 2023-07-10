#!/usr/bin/env bash
# exit on error
set -o errexit


python -m pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py createsuperuser  --no-input