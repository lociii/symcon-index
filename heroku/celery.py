# -*- coding: UTF-8 -*-
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heroku.settings')

app = Celery('heroku')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    'symcon_repository_update_nightly': {
        'task': 'symcon.tasks.symcon_repository_update_nightly',
        'schedule': crontab(hour=2, minute=0),
    },
}
