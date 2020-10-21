release: python manage.py migrate
web: python manage.py runserver 0:8080
worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
# web: gunicorn config.wsgi:application
# web: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
