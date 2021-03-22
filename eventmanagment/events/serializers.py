from rest_framework import serializers
from events.models import Event
from eventmanagment.users.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile_number')

class EventSerializer(serializers.ModelSerializer):
    owner = UserMinimalSerializer
    attendees = UserMinimalSerializer(many=True)
    class Meta:
        model = Event
        fields = '__all__'

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'date']