from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from . models import Event, FriendList, FriendRequest
from . serializers import EventSerializer, FriendListSerializer, FriendRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

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
    receiver = User.objects.get(id=current_user.id)
    friends = FriendListSerializer(FriendList.objects.all().filter(user=current_user), many=True).data
    friends_requests = FriendRequestSerializer(FriendRequest.objects.filter(receiver=receiver, is_active = True), many=True).data
    response_data = {}
    response_data['friends'] = friends
    response_data['friends_requests'] = friends_requests
    return Response(response_data)

@api_view(['POST'])
def send_friend_request(request):
    user = request.user
    username_receiver = request.data['username']
    receiver = User.objects.get(username=username_receiver)

    friend_request = FriendRequest(sender=user, receiver=receiver)
    friend_request.save()
    
    return Response(username_receiver)

@api_view(['POST'])
def accept_friend_request(request):
    current_user = request.user
    
    try:
        sender_id = request.data['id']
    except KeyError: 
        return HttpResponseBadRequest('id is required')
    
    # check is user exist sinon error 404
    # check si pas deja amis --> error 409
    sender = User.objects.get(id=sender_id)
    friend_request = FriendRequest.objects.filter(sender=sender, receiver=current_user).first()
    friend_request.accept()
    friend_request.delete()
    return Response(status.HTTP_201_CREATED)
    

@api_view(['DELETE'])
def remove_friend(request,id):
    """
    Remove friend
    """
    user = request.user
    friend_list = FriendList.objects.get(user=user)
    removee = User.objects.get(id=id)
    friend_list.unfriend(removee) # call method in model for remove friend of friend list
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def decline_friend_request(request,id):
    current_user = request.user
    sender = User.objects.get(id=id)
    friend_request = FriendRequest.objects.filter(sender=sender, receiver=current_user).first()
    friend_request.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)