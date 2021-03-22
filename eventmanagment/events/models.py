from django.db import models
from eventmanagment.users.models import User

# model for events
class Event(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    date = models.DateField(null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    owner = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='owner')
    attendees = models.ManyToManyField(User, related_name='attendees', null=True, blank=True)
    class Meta:
        app_label = 'events'