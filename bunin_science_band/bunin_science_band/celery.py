import os
from celery import Celery

# set the default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bunin_science_band.settings.prod")
app = Celery("bunin_science_band")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
