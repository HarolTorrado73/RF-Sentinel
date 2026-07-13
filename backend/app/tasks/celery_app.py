from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "sentinelrecon",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.task_routes = {
    "app.tasks.scan_tasks.*": {"queue": "scan_queue"},
}

celery_app.conf.task_track_started = True
celery_app.conf.task_time_limit = 3600