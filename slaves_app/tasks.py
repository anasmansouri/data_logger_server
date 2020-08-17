from celery.schedules import crontab
from celery.task import periodic_task
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def test_celery_worker():
    f = open("./demofile2.txt", "a")
    f.write("Now the file has more content!")
    f.close()
