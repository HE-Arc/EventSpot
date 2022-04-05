from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import status, viewsets, mixins, generics
from rest_framework.response import Response
from . models import Event, FriendList, FriendRequest, Profile, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from . serializers import EventSerializer, ProfileSerializer, BlacklistRefreshViewSerializer, FriendListSerializer, FriendRequestSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from django.db.models import Q
from django.conf import settings #this imports also your specific settings.py
from rest_framework.decorators import action

class OneByOneItems(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('count', self.page_size),
             ('total', self.page.paginator.count),
             ('current', self.page.number),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('results', data)
         ]))

class EventViewSet(viewsets.ModelViewSet):  
    model = Event
    serializer_class = EventSerializer
    pagination_class = OneByOneItems
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(user=user)
    
    @action(detail=False)
    def public(self, request):
        friendsList = FriendList.objects.get(user=request.user)
        events = Event.objects.all().filter(Q(user__id__in=friendsList.friends.all()) 
                                        | Q(is_private=False) 
                                        | Q(user=request.user)).distinct()
    
        serializer = EventSerializer(events,many=True)
    
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        #ici faut autoriser plus pour le retrieve
        #attention faut aussi verifier que pk existe sinon error 404
        #comme ça

        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        friendsList = FriendList.objects.get(user=request.user)
        eventsAuthorize = Event.objects.all().filter(Q(user__id__in=friendsList.friends.all()) 
                                            | Q(is_private=False) 
                                            | Q(user=request.user)).distinct()

        if event not in eventsAuthorize:
           return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = EventSerializer(event)
        return Response(serializer.data)   
      
@api_view(['GET'])
def search_users(request):
    username = request.GET.get('username')
    users = UserSerializer(User.objects.filter(username__startswith=username).order_by('username')[:5], many=True).data
    return Response(users)

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
        return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    

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
            if receiver == current_user:
                return Response({'message' : 'You cannot add yourself.'}, status=status.HTTP_409_CONFLICT)
            if not friend_list.is_friend(receiver):
                try:
                    # Test si l'utilisateur que l'on veut ajouté n'est pas déjà dans notre liste friend request                  
                    my_friend_requests = FriendRequest.objects.filter(receiver=current_user, sender=receiver)
                    for my_friend_request in my_friend_requests:
                        if my_friend_request:
                           return Response({'message' : 'A friend request has already been sent.'},status=status.HTTP_409_CONFLICT) 
                    
                    # Test si l'utilisateur que l'on veut ajouté a pas déjà reçu une friend request
                    friend_requests = FriendRequest.objects.filter(sender=current_user, receiver=receiver)
                    for request in friend_requests:
                        if request:
                            return Response({'message' : 'You already sent a friend request.'},status=status.HTTP_409_CONFLICT)                            
                    
                    friend_request = FriendRequest(sender=current_user, receiver=receiver)
                    friend_request.save()
                    return Response({'message' : 'Friend request sent.'},status=status.HTTP_201_CREATED)
                except FriendRequest.DoesNotExist:
                    friend_request = FriendRequest(sender=current_user, receiver=receiver)
                    friend_request.save()   
                    return Response({'message' : 'Friend request sent.'},status=status.HTTP_201_CREATED)
            else:
                return Response({'message' : 'You are already friend.'}, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    
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
                return Response({'message' : 'Friend request accepted.'},status.HTTP_201_CREATED)
            else:
                return Response({'message' : 'Something went wrong.'},status.HTTP_409_CONFLICT) 
        except User.DoesNotExist:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError: 
        return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)        
        
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
            return Response({'message' : 'Successfully removed that friend.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)   
    
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
            return Response({'message' : 'Friend request declined.'},status=status.HTTP_204_NO_CONTENT)   
        else:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST) 
    except User.DoesNotExist:
        return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)



class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):

    model = Profile

    def get_queryset(self):
        if self.action == 'create':
            user = self.request.user
            return Profile.objects.filter(user=user)
        else:
            return User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        if self.action == 'partial_update':
            return UserSerializer

        # default
        return ProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
  
    @action(detail=False)
    def myprofile(self, request):
        user = request.user
        queryset = Profile.objects.filter(user_id=user.id)
        serializer = ProfileSerializer(queryset, many=True)
        profile = serializer.data
        
        image = profile[0].get('profile_image')
        
        data = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'profile_image': image
        }
        
        return Response(data)


# This view must inherit from CreateAPIView otherwise CSRF abort
class BlacklistRefreshView(generics.CreateAPIView):
    serializer_class = BlacklistRefreshViewSerializer
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
