from celery import shared_task
from click import command
from wishes.celery  import app
import time 
from .management.commands.retrive_event_data import Command
from django.core.management import call_command



@shared_task
def sending_emails():
    call_command('retrive_event_data')