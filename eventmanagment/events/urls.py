from django.urls import include, path
from rest_framework import routers
from eventmanagment.events.views import EventList, EventDetail #EventViewSet

app_name = 'events'

urlpatterns = [
    path('', EventList.as_view()),
    path('<int:pk>/', EventDetail.as_view()),
]