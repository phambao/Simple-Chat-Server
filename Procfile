web: daphne django_channel.asgi:channel_layer  --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=django_channel.settings -v2