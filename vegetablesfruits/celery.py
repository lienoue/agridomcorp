# agriculture/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')

app = Celery('vegetablesfruits', broker='memory://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
