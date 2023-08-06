from django.db import models

# Create your models here.

class Employee(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'employee'
    
    def __str__(self):
        return self.name    

class EventType(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'eventtype'
    
    def __str__(self):
        return self.name
    
class Event(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE, related_name='event')
    event_type = models.ForeignKey(to=EventType, on_delete=models.CASCADE, related_name='event')
    event_date = models.DateField()
    
    class Meta:
        db_table = 'event'
    def __str__(self):
        return str(self.event_date)
    
    
class EmailTemplate(models.Model):
    event_type = models.OneToOneField(to=EventType, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = 'emailtemplate'
    
    def __str__(self):
        return self.subject
    
class EmailLog(models.Model):
    recipient_email = models.CharField(max_length= 100, null=True)
    subject = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=20, null=True)
    events = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.recipient_email} - {self.subject}"