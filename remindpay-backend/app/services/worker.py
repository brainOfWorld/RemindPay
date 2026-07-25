from celery import Celery
from celery.schedules import crontab
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "remindpay",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Lagos",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.conf.beat_schedule = {
    "check-due-reminders-every-minute": {
        "task": "app.services.worker.check_and_send_reminders",
        "schedule": crontab(minute="*"),
    },
    "check-overdue-invoices-hourly": {
        "task": "app.services.worker.check_overdue_invoices",
        "schedule": crontab(minute=0, hour="*"),
    },
}

celery_app.autodiscover_tasks(["app.services"])
