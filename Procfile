web: daphne django_channel.asgi:application  --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=django_channel.settings -v2