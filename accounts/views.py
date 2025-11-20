from django.contrib.auth import get_user_model
from rest_framework import (
    viewsets,
    permissions,
    status,
    mixins,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Notification
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    NotificationSerializer,
)
from .permissions import (
    UserViewPermission,
    NotificationPermission,
)

User = get_user_model()


# =========================
# JWT 로그인용 Serializer / View
# =========================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    필요 시 커스터마이징 (예: username 대신 email 로그인 등)
    지금은 기본 username/password를 사용합니다.
    """
    pass


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# =========================
# 회원/유저 관련 View
# =========================

class RegisterView(CreateAPIView):
    """
    회원가입
    POST /accounts/auth/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(RetrieveUpdateAPIView):
    """
    마이페이지 (본인 정보 조회/수정)
    GET /accounts/me/
    PATCH /accounts/me/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    - (매니저만) 모든 User 또는 조건부 User 조회
      GET /accounts/users/
        - 필터 예시: ?role=manager / ?role=instructor / ?name=홍길동 / ?email=...

    - (매니저와 User 본인만) 본인의 User 정보 수정
      PATCH /accounts/users/{id}/
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]

    def get_queryset(self):
        qs = super().get_queryset()

        # 매니저만 list 사용 가능 (permission에서 이미 체크)
        role = self.request.query_params.get('role')
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')

        if role:
            qs = qs.filter(role=role)
        if name:
            qs = qs.filter(name__icontains=name)
        if email:
            qs = qs.filter(email__icontains=email)

        return qs


# =========================
# Notification 관련 View
# =========================

class NotificationViewSet(viewsets.ModelViewSet):
    """
    Notification 관리

    - (매니저만)
        GET /accounts/notifications/        : 모든 알림 조회 (필터 가능)
        POST /accounts/notifications/       : 알림 생성 (특정 user 에게)
        PUT/PATCH/DELETE /accounts/notifications/{id}/ : 수정/삭제

    - (강사만)
        GET /accounts/notifications/        : 본인 알림만 조회
        GET /accounts/notifications/{id}/   : 본인 알림만 조회
        POST /accounts/notifications/{id}/mark-as-read/ : 읽음 처리
    """
    queryset = Notification.objects.select_related('user', 'lecture').all()
    serializer_class = NotificationSerializer
    permission_classes = [NotificationPermission]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.role == User.Role.MANAGER:
            # 매니저는 필터링 옵션 제공
            user_id = self.request.query_params.get('user_id')
            is_read = self.request.query_params.get('is_read')

            if user_id:
                qs = qs.filter(user_id=user_id)
            if is_read is not None:
                if is_read.lower() in ['true', '1']:
                    qs = qs.filter(is_read=True)
                elif is_read.lower() in ['false', '0']:
                    qs = qs.filter(is_read=False)
            return qs

        # 강사는 자신의 알림만
        return qs.filter(user=user)

    def perform_create(self, serializer):
        """
        매니저만 알림 생성 가능 (Permission에서 이미 체크)
        """
        serializer.save()

    @action(detail=True, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        """
        (강사/매니저) 알림 읽음 처리
        POST /accounts/notifications/{id}/mark-as-read/
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()

        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
