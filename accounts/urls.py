from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    MeView,
    CustomTokenObtainPairView,
    UserViewSet,
    NotificationViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # JWT Auth
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 회원가입
    path('auth/register/', RegisterView.as_view(), name='register'),

    # 마이페이지 (본인 정보)
    path('me/', MeView.as_view(), name='me'),

    # 기타 ViewSet
    path('', include(router.urls)),
]
