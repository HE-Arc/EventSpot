from django.urls import path,include
from . import views 
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet, basename='Event')
router.register(r'profiles', views.ProfileViewSet, basename='Profile')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/logout/', views.BlacklistRefreshView.as_view(), name="logout"),

    path('api/friends/create', views.send_friend_request, name='send_friend_request'),
    path('api/friends/accept', views.accept_friend_request, name='accept_friend_request'),
    path('api/friends/', views.friends_view, name='friends_view'),
    path('api/friends/search', views.search_users, name='search_users'),
    path('api/friends/<id>/delete', views.remove_friend, name='remove_friend'),
    path('api/friends/<id>/decline', views.decline_friend_request, name='decline_friend_request'),
  
    path('api/schema/', get_schema_view(
        title="Event Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),

    path('api/docs/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
  
    path('api/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
