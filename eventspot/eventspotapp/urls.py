from django.urls import path,include,re_path
from . import views 
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from rest_framework.schemas import get_schema_view
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
# Model routes
router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet, basename='Event')
router.register(r'profiles', views.ProfileViewSet, basename='Profile')
router.register(r'friends', views.FriendViewSet, basename='Friend')

# add doc and token
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/logout/', views.BlacklistRefreshView.as_view(), name="logout"),
    path('api/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
