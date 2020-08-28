python3 manage.py runserver &
celery -A principal worker &
celery -A principal beat &

