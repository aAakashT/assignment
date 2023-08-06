from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  EmailTemplateViewSet, EmployeeViewSet, EventTypeViewSet, EventViewSet
router = DefaultRouter()
router.register('api/emailtemplate', EmailTemplateViewSet, basename="emailtemplate")
router.register('api/employee', EmployeeViewSet, basename="employee")
router.register('api/eventtype', EventTypeViewSet, basename="eventtype")
router.register('api/event', EventViewSet, basename="event")


# print(router.urls)
urlpatterns = [
    path("", include(router.urls)),
]