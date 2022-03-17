from rest_framework.response import Response
from rest_framework import generics
from . models import Event, Profile, User
from . serializers import EventSerializer, CreateUserSerializer, UpdateUserSerializer, ChangePasswordSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class EventsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
    
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
        
        