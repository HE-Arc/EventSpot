from rest_framework import serializers
from eventspotapp.models import Event, User, Profile
from rest_framework.response import Response
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')
        
class BlacklistRefreshViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
                
class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    
    class Meta:
        model = Event
        fields = ('id','title','description','user','date','longitude','lattitude','image','is_private')
            
class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm')
        
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
        
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    profile_image = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'profile_image')
        
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value
        
    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        
        if 'profile_image' in validated_data:
            instance.profile.profile_image = validated_data['profile_image']
        
        instance.save()
        
        data = {
            'username': instance.username,
            'email': instance.email,
            'profile_image': instance.profile.profile_image
        }
        
        return data
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('password', 'confirm')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    
    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
        
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'