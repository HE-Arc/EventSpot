from dataclasses import fields
from email.policy import default
from tkinter.messagebox import NO
from urllib import request
from rest_framework import serializers
from eventspotapp.models import Event, FriendList
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
            