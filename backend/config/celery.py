from __future__ import absolute_import
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()    # Load task modules from all registered Django app configs.


@app.task(bind=True)
def debug_task(self):
    print(f'START Request: {self.request!r}')
