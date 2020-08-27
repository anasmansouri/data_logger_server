from celery.schedules import crontab
from celery.task import periodic_task
from celery import shared_task
from celery.utils.log import get_task_logger

from slaves_app.functions import read_sensors_values
from slaves_app.models import Slave

logger = get_task_logger(__name__)


@shared_task
def test_celery_worker():
    enabled_slaves = Slave.get_enabled_slaves()
    read_sensors_values(enabled_slaves)
    f = open("./log_file.txt", "a")
    f.write("value have been read successfully")
    f.close()
