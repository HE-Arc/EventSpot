from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('events/', views.EventsView.as_view(), name='events_view'),
    path('friends/create', views.send_friend_request, name='send_friend_request'),
    path('friends/accept', views.accept_friend_request, name='accept_friend_request'),
    path('friends/', views.friends_view, name='friends_view'),
    path('friends/search', views.search_users, name='search_users'),
    path('friends/<id>/delete', views.remove_friend, name='remove_friend'),
    path('friends/<id>/decline', views.decline_friend_request, name='decline_friend_request'),
]
