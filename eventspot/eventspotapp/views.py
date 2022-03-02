from rest_framework.response import Response
from rest_framework import generics
from . models import Event
from . serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class EventsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
        