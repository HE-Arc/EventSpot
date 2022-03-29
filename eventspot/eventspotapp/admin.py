from django.contrib import admin
from .models import Event, FriendList, FriendRequest, Profile

admin.site.register(Event)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(Profile)

