# Fishapp (Meenkari) - Local Development Setup

## Prerequisites

- Python 3.11+
- Git
- Virtual environment (already configured in `.venv`)

## Quick Start

### 1. Install Dependencies

The dependencies are already pinned in `requirements.txt`. If you need to reinstall:

```bash
cd /mnt/CURRENT/Fishapp/meenkari
/mnt/CURRENT/Fishapp/.venv/bin/pip install -r requirements.txt
```

### 2. Set up Environment Variables

```bash
cp .env.example .env
```

The `.env` file configures Django to run in development mode with a local SQLite database.

### 3. Run Migrations

```bash
/mnt/CURRENT/Fishapp/.venv/bin/python manage.py migrate
```

### 4. Create a Superuser (Optional)

```bash
/mnt/CURRENT/Fishapp/.venv/bin/python manage.py createsuperuser
```

### 5. Start the Development Server

```bash
cd /mnt/CURRENT/Fishapp/meenkari
bash run_dev.sh
```

Or manually:

```bash
/mnt/CURRENT/Fishapp/.venv/bin/daphne -b 0.0.0.0 -p 8000 meenkari.asgi:application
```

The server will start on `http://127.0.0.1:8000`

## Running Tests

```bash
/mnt/CURRENT/Fishapp/.venv/bin/python manage.py test meenkari.tests --verbosity=2
```

## Project Structure

- `meenkari/` - Main Django app
  - `models.py` - Game and Lobby database models
  - `game.py` - Core Fish game logic (move validation, scoring)
  - `assets.py` - Game helpers (shuffling, ID generation, websocket groups)
  - `views.py` - HTTP request handlers
  - `consumers.py` - WebSocket handlers
  - `templates/meenkari/` - HTML templates
  - `static/` - CSS, JavaScript, and images
  - `tests.py` - Regression tests for game logic

## Recent Improvements

✓ Settings now work without requiring `secret_settings.py`
✓ Fixed game ID uniqueness check (was comparing strings to querysets)
✓ Pinned dependencies to stable versions
✓ Removed `eval()` call in JavaScript (security improvement)
✓ Added regression tests for game helpers
✓ Improved exception handling in backend
✓ Database migrations working cleanly

## Known Limitations

- Channel layer uses in-memory backend (adequate for local dev, not suitable for multi-worker production deployments)
- CSRF exemption on game move endpoint needs review before production
- No user avatar support yet (placeholder "image" in nav)

## Next Steps

1. Add more comprehensive game logic tests
2. Modernize the frontend with better styling and UX
3. Add Redis channel layer for production deployments
4. Add analytics/replay functionality
5. Mobile responsiveness improvements

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
/mnt/CURRENT/Fishapp/.venv/bin/daphne -b 0.0.0.0 -p 8001 meenkari.asgi:application
```

### Database Issues

Reset the database (deletes all data):

```bash
rm db.sqlite3
/mnt/CURRENT/Fishapp/.venv/bin/python manage.py migrate
```

### Import Errors

Make sure the virtual environment is activated and dependencies are installed:

```bash
/mnt/CURRENT/Fishapp/.venv/bin/pip install -r requirements.txt
```
