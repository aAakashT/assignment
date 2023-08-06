from celery.schedules import crontab
from .task import sending_emails

CELERY_BEAT_SCHEDULE = {
    'run_custom_command_daily': {
        'task': 'wishing_app.tasks.sending_emails',
        'schedule': crontab(hour=0, minute=0)
    },
}