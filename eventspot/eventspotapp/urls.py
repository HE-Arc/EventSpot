from django.urls import path
from . views import EventsView, CreateProfileView, CreateProfileView, DetailProfileView, UpdateProfileView, UpdatePasswordView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('events/', EventsView.as_view(), name='events_view'),
    path('profiles/', CreateProfileView.as_view(), name='createProfile_view'),
    path('profile/', DetailProfileView.as_view(), name='showProfile_view'),
    path('profiles/update/<int:pk>/', UpdateProfileView.as_view(), name='updateProfile_view'),
    path('profiles/password/<int:pk>/', UpdatePasswordView.as_view(), name='updatePassword_view'),
]
