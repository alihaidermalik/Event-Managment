from django.shortcuts import render
from events.models import Event
from events.forms import EventForm
from .serializers import EventSerializer, EventListSerializer
from rest_framework import viewsets
from eventmanagment.users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

class EventList(generics.ListAPIView):
    queryset = Event.objects.prefetch_related('attendees').select_related("owner").all()
    serializer_class = EventListSerializer


class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.prefetch_related('attendees').select_related("owner").all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)

    # def event_exists(self, pk):
    #     filter_event = Event.objects.filter(id=pk)
    #     if filter_event.exists():
    #         return filter_event.last()

    # def is_owner(self, request, pk):
    #     event = Event.objects.get(id=pk)
    #     user = request.user
    #     if user == event.owner:
    #         return True
    #     else:
    #         return False

    def delete(self, request, pk):
        filter_event = Event.objects.filter(id=pk)
        if filter_event.exists():
            event = filter_event.last()
            user = request.user
            if user == event.owner:
                event.delete()
                return Response({"detail":"deleted sucessfully"})
            else:
                return Response({"detail":"you are not owner of this event"})
        else:
            return Response({"detail":"event not found"})
    
    def put(self, request, pk):
        filter_event = Event.objects.filter(id=pk)
        if filter_event.exists():
            event = Event.objects.get(id=pk)
            user = request.user
            if user == event.owner:
                event.title = request.data.get('title', event.title)
                event.date = request.data.get('date', event.date)
                event.description = request.data.get('date', event.description)
                event.location = request.data.get('location', event.location)
                event.save()
                attendees = request.data.get('attendees', None)
                # event.event.update(title=title, date=date, description=description, location=location)

                if attendees:
                    for guest in attendees:
                        try:
                            attendee = User.objects.get(username=guest)
                            event.attendees.add(attendee)
                        except:
                            return Response({"detail":"Invalid attendee name "+guest})

                return Response({"detail":"updated sucessfully"})
            else:
                return Response({"detail":"you are not owner of this event"})
        else:
            return Response({"detail":"event not found"})

