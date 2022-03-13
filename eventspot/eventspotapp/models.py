from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event (models.Model):
    
    title = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
class FriendList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends") 
    
    def __str__(self):
        return self.user.username
    
    def add_friend(self, account): # user ? 
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            
    def remove_friend(self,account):
        """
        Remove a friend
        """
        if account in self.friends.all():
            self.friends.remove(account)
    
    def unfriend(self,removee):
        """
        Initiate the action of unfriending
        """
        remover_friends_list = self
        
        remover_friends_list.remove_friend(removee)
        
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)
        
    def is_friend(self, friend):
        """
        Is this a friend ?
        """
        if friend in self.friends.all():
            return True
        return False
    
    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False 
    