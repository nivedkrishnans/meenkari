#!/bin/bash
# Local development server startup script

set -e

cd "$(dirname "$0")" || exit

# Activate venv if needed
if [ -f ../.venv/bin/activate ]; then
    source ../.venv/bin/activate
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start the development server
echo "Starting Daphne server on 0.0.0.0:8000"
echo "Visit: http://127.0.0.1:8000"
echo ""

daphne -b 0.0.0.0 -p 8000 meenkari.asgi:application
