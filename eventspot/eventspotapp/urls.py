from django.urls import path
from . import views 
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token-refresh/', TokenRefreshView.as_view()),
    path('api/token-logout/', views.BlacklistRefreshView.as_view(), name="logout"),

    path('api/friends/create', views.send_friend_request, name='send_friend_request'),
    path('api/friends/accept', views.accept_friend_request, name='accept_friend_request'),
    path('api/friends/', views.friends_view, name='friends_view'),
    path('api/friends/search', views.search_users, name='search_users'),
    path('api/friends/<id>/delete', views.remove_friend, name='remove_friend'),
    path('api/friends/<id>/decline', views.decline_friend_request, name='decline_friend_request'),
  
    path('api/profiles/', views.CreateProfileView.as_view(), name='createProfile_view'),
    path('api/profile/', views.DetailProfileView.as_view(), name='showProfile_view'),
    path('api/profiles/update/<int:pk>/', views.UpdateProfileView.as_view(), name='updateProfile_view'),
    path('api/profiles/password/<int:pk>/', views.UpdatePasswordView.as_view(), name='updatePassword_view'),
  
    path('api/events/create', views.event_create, name='events_create'),
    path('api/events/public', views.public_event_list, name='events_list'),
    path('api/events/', views.my_event_list, name='events_list'),
    path('api/events/<id>', views.event_detail, name='events_detail'),
    path('api/events/<id>/delete', views.event_detail, name='events_delete'),
    path('api/events/<id>/update', views.event_detail, name='events_update'),
  
    path('api/schema/', get_schema_view(
        title="Event Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),
  
    path('api/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
