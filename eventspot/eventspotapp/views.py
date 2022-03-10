from rest_framework.response import Response
from rest_framework import generics
from . models import Event, User
from . serializers import EventSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class EventsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
    
class CreateProfileView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        