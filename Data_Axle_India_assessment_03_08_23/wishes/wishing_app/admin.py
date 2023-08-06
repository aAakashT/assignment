from django.contrib import admin
from .models import EmailTemplate, Employee, Event, EventType
# Register your models here.
admin.site.register([EmailTemplate, Employee, Event, EventType])
