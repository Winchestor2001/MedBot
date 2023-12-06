import os

from celery import Celery
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

minute = 10

app.conf.beat_schedule = {
    f'check-meet-every-{minute}-minute': {
        'task': 'med_app.tasks.check_meet',
        'schedule': timedelta(minutes=minute),
    }
}
