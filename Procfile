web: gunicorn django_analytics.wsgi --log-file -
web: daphne meenkari.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
