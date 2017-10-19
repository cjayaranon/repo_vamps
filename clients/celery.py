from __future__ import absolute_import
import os
import django
from celery import Celery
from django.conf import settings
 
# Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vamps.settings')
 
app = Celery('vamps')
app.config_from_object('django.conf:settings', namespace='CELERY')
# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))