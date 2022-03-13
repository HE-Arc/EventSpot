from rest_framework import serializers
from eventspotapp.models import Event
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')
        
class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    
    class Meta:
        model = Event
        fields = ('id','title','description','user','date','longitude','lattitude','image')
        
