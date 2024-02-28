import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("camp-python-2022-ibid-these")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
