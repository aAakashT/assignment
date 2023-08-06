import logging
from django.core.management.base import BaseCommand
from ...views import send_email_to_employee

class Command(BaseCommand):
    help = "Retrives event data from the event and send email"
    
    def handle(self, *args, **kwargs):
        send_email_to_employee()
        