web: gunicorn mysite.wsgi --log-file -
celery: python manage.py celery worker -E -B--time-limit=1200 -Q celery,slow,search