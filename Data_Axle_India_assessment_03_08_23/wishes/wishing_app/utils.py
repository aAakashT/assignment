import logging
from .models import EmailLog

def log_email_event(recipient_email=None, subject=None, status=None, events=True, error_message=None):
    logger = logging.getLogger('email_events')
    
    log_msg = f"Recipient: {recipient_email}, Subject: {subject}, Status: {status}"
    if error_message:
        log_msg += f", Error: {error_message}"

    if status == 'SUCCESS':
        logger.info(log_msg)
    else:
        logger.error(log_msg)

    EmailLog.objects.create(
        recipient_email=recipient_email,
        subject=subject,
        status=status,
        events=events,
        error_message=error_message,
    )
    # print(EmailLog.objects.all())