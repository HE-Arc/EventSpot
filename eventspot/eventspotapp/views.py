from telnetlib import STATUS
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from . models import Event, FriendList
from . serializers import EventSerializer, FriendListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

# Create your views here.
class EventsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def friends_view(request):
    current_user = request.user
    list_friends = FriendList.objects.all().filter(user=current_user)
    serializer = FriendListSerializer(list_friends,many=True)
    return Response(serializer.data)
