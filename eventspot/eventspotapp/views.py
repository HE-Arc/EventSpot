from multiprocessing import context
from django.http import HttpResponseBadRequest
from rest_framework import status, viewsets, mixins, generics
from rest_framework.response import Response
from . models import Event, FriendList, FriendRequest, Profile, User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from . serializers import EventSerializer, ProfileSerializer, BlacklistRefreshViewSerializer, FriendListSerializer, FriendRequestSerializer, UserSerializer,ProfileUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from django.db.models import Q
from rest_framework.decorators import action
from django.utils import timezone

class OneByOneItems(PageNumberPagination):
    """
    Custum pagination
    """
    
    # 6 items by page
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
    permission_classes = [IsAuthenticated] # only if the user is authenticated
    
    
    def get_queryset(self):
        """
        Working only on our events
        """
        user = self.request.user
        return Event.objects.filter(user=user)
    
    @action(detail=False)
    def public(self, request):
        """
        Get public events
        A public event is our event, our friends event and public events 
        """
        friendsList = FriendList.objects.get(user=request.user)
        events = Event.objects.all().filter(Q(user__id__in=friendsList.friends.all()) 
                                        | Q(is_private=False) 
                                        | Q(user=request.user)).filter(end_date__gte=timezone.now()).distinct()
    
        serializer = EventSerializer(events, many=True)
    
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """
        Assign the current event when creating an event
        """
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a public event
        """
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) # Event not found

        # Retrieve our friend
        friendsList = FriendList.objects.get(user=request.user)
        
        # Get all public events
        eventsAuthorize = Event.objects.all().filter(Q(user__id__in=friendsList.friends.all()) 
                                            | Q(is_private=False) 
                                            | Q(user=request.user)).distinct()

        if event not in eventsAuthorize:
           return Response(status=status.HTTP_403_FORBIDDEN) # Forbidden if the event is not in public event
        
        serializer = EventSerializer(event)
        
        return Response(serializer.data)   

class FriendViewSet(viewsets.ModelViewSet):  
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        """
        Get all friends and friend request of the current user
        """
        try:
            current_user = request.user
            receiver = User.objects.get(id=current_user.id)
            try:
                friends = FriendListSerializer(FriendList.objects.all().filter(user=current_user), many=True).data
                friends_requests = FriendRequestSerializer(FriendRequest.objects.filter(receiver=receiver), many=True).data
                
                # Join data to get friends and friend request on 1 time
                response_data = {}
                response_data['friends'] = friends
                response_data['friends_requests'] = friends_requests
                return Response(response_data)
            
            except (friends.DoesNotExist, friends_requests.DoesNotExist) as e:
                return HttpResponseBadRequest(e)        
        except User.DoesNotExist:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def create(self,request):
        """
        Create a friend request
        """
        
        # Get the current user
        current_user = request.user
        try:    # If the current user and the new friend exist 
            username_receiver = request.data['username']
            receiver = User.objects.get(username=username_receiver)
            friend_list = FriendList.objects.get(user=current_user)
            
            # if the current user is the new user
            if receiver == current_user:
                return Response({'message' : 'You cannot add yourself.'}, status=status.HTTP_409_CONFLICT)
            
            # if the new user is not already in our friend list request
            if not friend_list.is_friend(receiver):
                
                # if this friend is already in my friend request
                my_friend_requests = FriendRequest.objects.filter(receiver=current_user, sender=receiver)
                for my_friend_request in my_friend_requests:
                    if my_friend_request:
                        return Response({'message' : 'A friend request has already been sent.'},status=status.HTTP_409_CONFLICT) 
                
                # if this friend has already got my friend request
                friend_requests = FriendRequest.objects.filter(sender=current_user, receiver=receiver)
                for request in friend_requests:
                    if request:
                        return Response({'message' : 'You already sent a friend request.'},status=status.HTTP_409_CONFLICT)                            
                
                # no conflict so we create the friend request
                friend_request = FriendRequest(sender=current_user, receiver=receiver)
                friend_request.save()
                return Response({'message' : 'Friend request sent.'},status=status.HTTP_201_CREATED)
            else:
                return Response({'message' : 'You are already friend.'}, status=status.HTTP_409_CONFLICT)
        except (KeyError, User.DoesNotExist) as e:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def destroy(self,request,pk=None):
        """
        Remove a friend
        """
        current_user = request.user
        try:
            user_to_remove = User.objects.get(id=pk)
            friend_list = FriendList.objects.get(user=current_user)
            
            # check if we are friend with the user to remove
            if friend_list.is_friend(user_to_remove): 
                friend_list.unfriend(user_to_remove)
                return Response({'message' : 'Successfully removed that friend.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST) 
                
            
    @action(detail=False)
    def search(self, request):
        """
        Search 5 first user 
        ing with the username received in the request
        """
        username = request.GET.get('username')
        users = UserSerializer(User.objects.filter(username__istartswith=username).order_by('username')[:5], many=True).data
        return Response(users)

    @action(detail=True, methods=['delete'])
    def decline(self, request,pk=None):
        """
        Decline a friend request
        """
        current_user = request.user
        try:  
            sender = User.objects.get(id=pk)
            friend_request = FriendRequest.objects.filter(sender=sender, receiver=current_user).first()
            
            # Check if the friend request exist
            if friend_request:
                friend_request.delete()
                return Response({'message' : 'Friend request declined.'},status=status.HTTP_204_NO_CONTENT)   
            else:
                return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST) 
        except User.DoesNotExist:
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(detail=False, methods=['post'])
    def accept(self, request):
        """
        Accept a friend request
        """
        current_user = request.user
        try:
            sender_id = request.data['id']
            sender = User.objects.get(id=sender_id)
            friend_request = FriendRequest.objects.filter(sender=sender, receiver=current_user).first()
            
            # accept only if a request has been sent
            if friend_request:
                friend_request.accept() # accept friend
                friend_request.delete() # remove user from friend request list
                return Response({'message' : 'Friend request accepted.'},status.HTTP_201_CREATED)
            else:
                return Response({'message' : 'Something went wrong.'},status.HTTP_409_CONFLICT) 
        except (KeyError,User.DoesNotExist) as e: 
            return Response({'message' : 'User not found.'}, status=status.HTTP_400_BAD_REQUEST) 
              



class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    Only create and update
    """
    model = Profile

    def get_queryset(self):
        """
        Return different model on specific action
        """
        if self.action == 'create':
            user = self.request.user
            return Profile.objects.filter(user=user)
        else:
            return User.objects.all()
    
    def get_serializer_class(self):
        """
        Return different serializer on specific action
        """
        if self.action == 'create' or self.action == 'partial_update':
            return ProfileUserSerializer

        # default
        return ProfileSerializer

    def get_permissions(self):
        """
        Return different permission on specific action
        """
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super(ProfileViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
  
    @action(detail=False)
    def myprofile(self, request):
        """
        Allow to retrieve user information with profil
        """
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
