from django.test import TestCase
from datetime import date, timedelta
from django.core import mail
from .models import Event, EventType,  Employee, EmailTemplate
from .views import send_email_to_employee
from io import StringIO
import logging
import sys
# Create your tests here.

class EmailSendingTest(TestCase):
    def setUp(self):
        event_date = date.today()
        self.event1 = EventType.objects.create(name='Birthday')
        self.event2 = EventType.objects.create(name='Work Anniversary')
        EmailTemplate.objects.create(event_type=self.event1, subject='Happy Birthday', content=f',\nWishing you a fantastic birthday on {event_date}!')
        EmailTemplate.objects.create(event_type=self.event2, subject='Happy Work Anniversary', content=f',\nWishing you a fantastic Work Anniversary on {event_date}!')
        Employee.objects.create(name='Ethan Hunt', email='aakashthorve66@gmail.com')

    def test_send_emails_on_event_date(self):
        event_date = date.today()
        Event.objects.create(employee_id=1, event_type=self.event1, event_date=event_date)

        send_email_to_employee()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Happy Birthday')
        self.assertIn('hi Ethan Hunt', mail.outbox[0].body)
        self.assertIn(str(event_date), mail.outbox[0].body)

    def test_no_events_scheduled(self):
        captured_output = StringIO()
        logger = logging.getLogger('wishing_app.views')
        logger.addHandler(logging.StreamHandler(captured_output))

        send_email_to_employee()
        
        sys.stdout = sys.__stdout__
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn("No events are scheduled for the current period.", captured_output.getvalue())

    def test_email_sending_exception(self):
        event_date = date.today() - timedelta(days=1)
        Event.objects.create(employee_id=1, event_type=self.event1, event_date=event_date)
        captured_output = StringIO()
        logger = logging.getLogger('wishing_app.views')
        logger.addHandler(logging.StreamHandler(captured_output))

        send_email_to_employee()
        sys.stdout = sys.__stdout__
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn("No events are scheduled for the current period.", captured_output.getvalue())

    def test_multiple_events_on_same_date(self):
        event_date = date.today()
        Event.objects.create(employee_id=1, event_type=self.event1, event_date=event_date)
        Event.objects.create(employee_id=1, event_type=self.event2, event_date=event_date)

        send_email_to_employee()

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Happy Birthday')
        self.assertIn('hi Ethan Hunt', mail.outbox[0].body)
        self.assertIn(str(event_date), mail.outbox[0].body)
        self.assertEqual(mail.outbox[1].subject, 'Happy Work Anniversary')
        self.assertIn('hi Ethan Hunt', mail.outbox[1].body)
        self.assertIn(str(event_date), mail.outbox[1].body)

    
    def test_last_successful_execution_time(self):
        today_event = date.today()
        tomorrow_event = date.today() + timedelta(days=1)
        Event.objects.create(employee_id=1, event_type=self.event1, event_date=today_event)
        Event.objects.create(employee_id=1, event_type=self.event2, event_date=tomorrow_event)

        send_email_to_employee()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Happy Birthday')
        self.assertIn('hi Ethan Hunt', mail.outbox[0].body)
        self.assertIn(str(today_event), mail.outbox[0].body)

        send_email_to_employee()

        self.assertEqual(len(mail.outbox), 2)

    def tearDown(self):
        mail.outbox = []
