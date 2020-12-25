release: python manage.py migrate
# web: python manage.py runserver 0:8080
web: python manage.py compress && gunicorn config.wsgi:application --bind 0.0.0.0:8080
worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
