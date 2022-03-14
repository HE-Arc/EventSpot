from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Event (models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,default="")
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    lattitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(upload_to='uploads/')
    is_private = models.BooleanField(default=False)


    def __str__(self):
        return self.title