from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import os

class Event (models.Model):
    """
    Model containing events,
    each event is owned by a user
    """

    user =  models.ForeignKey(User, on_delete=models.CASCADE,default="")
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    lattitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(upload_to='uploads/',blank =True)
    is_private = models.BooleanField(default=False)
        
    def __str__(self):
        return self.title
    
class FriendList(models.Model):
    """
    Model containing friends of the current userr
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends") 
    
    def __str__(self):
        return self.user.username
    
    def add_friend(self, new_friend):
        """
        Add a new friend
        """
        if not new_friend in self.friends.all():
            self.friends.add(new_friend)
            
    def remove_friend(self,friend):
        """
        Remove a friend
        """
        if friend in self.friends.all():
            self.friends.remove(friend)
    
    def unfriend(self,friend_to_remove):
        """
        Initiate the action of unfriending
        """
        remover_friends_list = self
        
        remover_friends_list.remove_friend(friend_to_remove)
        
        friends_list = FriendList.objects.get(user=friend_to_remove)
        friends_list.remove_friend(self.user)
        
    def is_friend(self, friend):
        """
        Is this a friend ?
        """
        if friend in self.friends.all():
            return True
        return False
    
class FriendRequest(models.Model):
    """
    Model containing friend request
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self):
        return self.sender.username
    
    def accept(self):
        """
        Accept a friend request
        """
        
        # get user friend list
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            # add friend
            receiver_friend_list.add_friend(self.sender)
            # get friend list 
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                # add self in his friend list
                sender_friend_list.add_friend(self.receiver)
                self.save()
        
class Profile(models.Model):
    """
    Model extending user for adding profile image
    Relation 1-1
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='uploads/',blank =True)


### Receivers
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    After create a user create a profile
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    After update a user update a profile
    """
    instance.profile.save()

@receiver(pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Profile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Profile.objects.get(pk=instance.pk).profile_image
        new_file = instance.profile_image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except:
        return False

@receiver(post_delete, sender=Event)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Event` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Event)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Event` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Event.objects.get(pk=instance.pk).image
        new_file = instance.image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except :
        return False
