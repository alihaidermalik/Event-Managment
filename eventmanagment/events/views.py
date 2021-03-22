from django.shortcuts import render
from events.models import Event
from .serializers import EventSerializer, EventListSerializer
from rest_framework import viewsets
from eventmanagment.users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.timezone import datetime

class EventList(generics.ListAPIView):
    queryset = Event.objects.prefetch_related('attendees').select_related("owner").all()
    serializer_class = EventListSerializer

    def post(self, request):
        owner = request.user
        title = request.data.get('title', 'No name')
        date = request.data.get('date', datetime.today())
        description = request.data.get('description', '')
        location = request.data.get('location', '')
        event = Event.objects.create(title=title, date=date, description=description, location=location, owner=owner)
        attendees = request.data.get('attendees', None)
        if attendees:
            for guest in attendees:
                try:
                    attendee = User.objects.get(username=guest)
                    event.attendees.add(attendee)
                except:
                    return Response({"detail":"Invalid attendee name "+guest})

        return Response({"detail":"created sucessfully"})




class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.prefetch_related('attendees').select_related("owner").all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)

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
                event.description = request.data.get('description', event.description)
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

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def attend_event_endpoint(request, pk):
    filter_event = Event.objects.filter(id=pk)
    if filter_event.exists():
        if filter_event.filter(attendees=request.user):
            return Response({"detail":"You are already in the list"})
        event = Event.objects.get(id=pk)
        event.attendees.add(request.user)
        return Response({"detail":"Congrates you are added to the list."})
    else:
        return Response({"detail":"event not found"})
