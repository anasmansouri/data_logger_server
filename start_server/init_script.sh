cd ..
python3 manage.py runserver &
celery -A principal worker &
celery -A principal beat > /dev/null 2>&1 &

