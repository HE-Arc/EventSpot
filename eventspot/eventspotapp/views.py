from django.http import HttpResponseBadRequest
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
    """
    view list of friends and friends requests
    """
    try:
        current_user = request.user
        receiver = User.objects.get(id=current_user.id)
        try:
            friends = FriendListSerializer(FriendList.objects.all().filter(user=current_user), many=True).data
            friends_requests = FriendRequestSerializer(FriendRequest.objects.filter(receiver=receiver), many=True).data
            response_data = {}
            response_data['friends'] = friends
            response_data['friends_requests'] = friends_requests
            return Response(response_data)
        
        except (friends.DoesNotExist, friends_requests.DoesNotExist) as e:
            return HttpResponseBadRequest(e)        
    except User.DoesNotExist:
        return HttpResponseBadRequest("User invalid")
    

@api_view(['POST'])
def send_friend_request(request):
    """
    send friend request
    """
    current_user = request.user
    try:
        username_receiver = request.data['username']
        try:
            receiver = User.objects.get(username=username_receiver)
            friend_list = FriendList.objects.get(user=current_user)
            if not friend_list.is_friend(receiver):
                try:
                    friend_requests = FriendRequest.objects.filter(sender=current_user, receiver=receiver)
                    for request in friend_requests:
                        if request:
                            return HttpResponseBadRequest("You already sent them a friend request.")
                    friend_request = FriendRequest(sender=current_user, receiver=receiver)
                    friend_request.save()
                    return Response(status=status.HTTP_201_CREATED)
                except FriendRequest.DoesNotExist:
                    friend_request = FriendRequest(sender=current_user, receiver=receiver)
                    friend_request.save()   
                    return Response(status=status.HTTP_201_CREATED)
            else:
                return HttpResponseBadRequest("Already friend")
        except User.DoesNotExist:
            return HttpResponseBadRequest("User invalid")
    except KeyError:
        return HttpResponseBadRequest('User invalid')
    
@api_view(['POST'])
def accept_friend_request(request):
    """
    accept friend request
    """
    current_user = request.user
    try: # Test si l'id a été envoyé
        sender_id = request.data['id']
        try: # Test si l'utilisateur est existant
            sender = User.objects.get(id=sender_id)
            friend_request = FriendRequest.objects.filter(sender=sender, receiver=current_user).first()
            if friend_request: # Test si c'est le bon utilisateur qui a envoyé la demande
                friend_request.accept()
                friend_request.delete()
                return Response(status.HTTP_201_CREATED)
            else:
                return Response(status.HTTP_409_CONFLICT) 
        except User.DoesNotExist:
            return HttpResponseBadRequest("User invalid")
    except KeyError: 
        return HttpResponseBadRequest('User invalid')        
        
@api_view(['DELETE'])
def remove_friend(request,id):
    """
    Remove friend
    """
    current_user = request.user
    try:
        removee = User.objects.get(id=id)
        friend_list = FriendList.objects.get(user=current_user)
        if friend_list.is_friend(removee): # check if friend with the removee
            friend_list.unfriend(removee) # call method in model for remove friend of friend list
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponseBadRequest("User not found")
    except User.DoesNotExist:
        return HttpResponseBadRequest('User invalid')     
    
@api_view(['DELETE'])
def decline_friend_request(request,id):
    """
    Decline friend request
    """
    current_user = request.user
    try:  
        sender = User.objects.get(id=id)
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=current_user).first()
        if friend_request:
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)   
        else:
            return HttpResponseBadRequest("User not found") 
    except User.DoesNotExist:
        return HttpResponseBadRequest('User invalid') 
