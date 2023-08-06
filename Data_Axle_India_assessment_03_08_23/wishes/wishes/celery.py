
import os 
from celery import Celery
from celery.schedules import crontab
# from ..wishing_app import  managemmet.commands.retrive_event_data as my_custom_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "wishes.settings")
app = Celery('wishes')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """This function schedules the task to run every day at 12 AM."""
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        'wishing_app.task.sending_emails',
    )

if __name__ == '__main__':
    app.start()