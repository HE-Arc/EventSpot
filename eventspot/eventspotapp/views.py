from rest_framework.response import Response
from rest_framework import generics
from . models import Event
from . serializers import EventSerializer

# Create your views here.
class EventsView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
        