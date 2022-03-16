from email.policy import default
from tkinter.messagebox import NO
from rest_framework import serializers
from eventspotapp.models import Event, FriendList, FriendRequest
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
class FriendListSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True, read_only=True)
    class Meta:
        model = FriendList
        fields = ('id','user','friends')
        
class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    class Meta:
        model = FriendRequest
        fields = ('id','is_active','timestamp', 'receiver', 'sender')
            