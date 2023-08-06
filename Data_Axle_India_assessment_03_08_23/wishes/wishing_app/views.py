from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Event, Employee, EmailTemplate, EventType, EmailLog
from .serializers import EventSerializer, EmployeeSerializer, EmailTemplateSerializer, EventTypeSerializer
import datetime
from .utils import log_email_event
from django.core.mail import send_mail
from django.core import mail
import logging

# Create your views here.

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
class EventTypeViewSet(ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
class EmailTemplateViewSet(ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    
logger = logging.getLogger('wishing_app.views')
logger.setLevel(logging.INFO)


def send_email_to_employee():
    events = Event.objects.filter(event_date__endswith=datetime.date.today().strftime("%m-%d")).prefetch_related("employee", "event_type")
    if events:
        for event in events:
            emailid  = event.employee.email
            emp_name = event.employee.name
            event_type = event.event_type.id
            try:
                template = EmailTemplate.objects.get(event_type=event_type)
                subject = template.subject
                content = "hi " + emp_name + template.content
            except EmailTemplate.DoesNotExist as e:
                pass
            def sender():
                """sender function will try to send mail 3 times and then it will log error or sucess in db
                please change sender email to your email"""
                count = 0
                while True:
                    try:
                        res = send_mail(subject=subject, message=content, from_email='thoraveaakash0@gmail.com', recipient_list=[emailid,], fail_silently=False)
                        return True
                    except Exception as e:
                        count += 1
                        if count == 3:
                            log_email_event(emailid, subject, 'ERROR', e)
                            return False
            res = sender()
            if res == True:
                log_email_event(emailid, subject, 'SUCCESS')
                logger.info(f"Sucess to send email to {emailid}")
            if res == False:
                logger.error(f"Failed to send email to {emailid}")
    else:
        log_email_event(events=False)
        logger.error("No events are scheduled for the current period.")
        return "No events are scheduled for the current period."
