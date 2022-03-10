from django.urls import path
from . views import EventsView, CreateProfileView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('events/', EventsView.as_view(), name='events_view'),
    path('profiles/', CreateProfileView.as_view(), name='createProfile_view'),
]
