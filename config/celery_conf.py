import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery("qr_menu_api")

celery_app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

celery_app.autodiscover_tasks()
