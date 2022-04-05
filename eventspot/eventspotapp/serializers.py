from dataclasses import field
from email.policy import default
from tkinter.messagebox import NO
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from eventspotapp.models import Event, FriendList, FriendRequest, User, Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id','username', 'profile')
                
class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ('id','title','description','user','date','longitude','lattitude','image','is_private')
        
class FriendListSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True, read_only=True)
    class Meta:
        model = FriendList
        fields = ('id','user','friends')
        
class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    class Meta:
        model = FriendRequest
        fields = ('id','receiver', 'sender')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="This email is already in use."
        )]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="This username is already in use."
        )]
    )

    password = serializers.CharField(write_only=True, required=True)
    confirm = serializers.CharField(write_only=True, required=True)
    profile_image = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm', 'profile_image')
    
    def validate(self, attrs):
        if 'password' in attrs:
            if attrs['password'] != attrs['confirm']:
                raise serializers.ValidationError({"password": "Password fields don't match."})

        return attrs
        
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        FriendList.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        if 'username' in validated_data:
            instance.username = validated_data['username']
        
        if 'email' in validated_data:
            instance.email = validated_data['email']
        
        if 'profile_image' in validated_data:
            instance.profile.profile_image = validated_data['profile_image']
        
        instance.save()
        
        data = {
            'username': instance.username,
            'email': instance.email,
            'profile_image': instance.profile.profile_image,  
        }
        
        return data

class BlacklistRefreshViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'