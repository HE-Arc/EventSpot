from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from . models import Event, FriendList, FriendRequest,Profile, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from . serializers import EventSerializer, CreateUserSerializer, UpdateUserSerializer, ChangePasswordSerializer, ProfileSerializer,BlacklistRefreshViewSerializer,FriendListSerializer, FriendRequestSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

class BlacklistRefreshView(generics.CreateAPIView):
    serializer_class = BlacklistRefreshViewSerializer
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")

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
        
@api_view(['GET'])
def event_list(request):
    """
    Retrieve all events
    """
    paginator = OneByOneItems()

    events = Event.objects.all()
    context = paginator.paginate_queryset(events, request)

    serializer = EventSerializer(context,many=True)
    
    return paginator.get_paginated_response(serializer.data)
   

@api_view(['POST'])
def event_create(request):
    """
    Create a new event
    """    
    serializer = EventSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, id):
    """
    Retrieve, update or delete an event.
    """
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      
@api_view(['GET'])
def search_users(request):
    users = UserSerializer(User.objects.all(), many=True).data
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
                    friend_requests = FriendRequest.objects.filter(sender=current_user, receiver=receiver)
                    for request in friend_requests:
                        if request:
                            return Response({'message' : 'You already sent them a friend request.'},status=status.HTTP_409_CONFLICT)
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
    
class CreateProfileView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class DetailProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    
    def get(self, request, *args, **kwargs):       
        user = request.user
        queryset = Profile.objects.filter(user_id=user.id)
        serializer = ProfileSerializer(queryset, many=True)
        profile = serializer.data
        
        image = profile[0].get('profile_image')
        if image is not None:
            image = 'http://localhost:8000' + image
        
        data = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'profile_image': image
        }
        
        return Response(data)
    
class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class UpdatePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
