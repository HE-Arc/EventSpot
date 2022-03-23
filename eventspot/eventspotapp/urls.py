from django.urls import path
from . import views 
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('api-token-logout/', views.BlacklistRefreshView.as_view(), name="logout"),
    path('profiles/', views.CreateProfileView.as_view(), name='createProfile_view'),
    path('profile/', views.DetailProfileView.as_view(), name='showProfile_view'),
    path('profiles/update/<int:pk>/', views.UpdateProfileView.as_view(), name='updateProfile_view'),
    path('profiles/password/<int:pk>/', views.UpdatePasswordView.as_view(), name='updatePassword_view'),
    path('events/create', views.event_create, name='events_create'),
    path('events/', views.event_list, name='events_list'),
    path('events/<id>', views.event_detail, name='events_detail'),
    path('events/<id>/delete', views.event_detail, name='events_delete'),
    path('events/<id>/update', views.event_detail, name='events_update'),
    path('openapi/', get_schema_view(
        title="Event Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
