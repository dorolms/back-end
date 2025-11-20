from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsManager(permissions.BasePermission):
    """
    매니저만 접근 가능
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, 'role', None) == User.Role.MANAGER
        )


class UserViewPermission(permissions.BasePermission):
    """
    UserViewSet 전용 권한:

    - list  : 매니저만
    - retrieve: 매니저 또는 본인
    - update/partial_update: 본인만
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if getattr(view, 'action', None) == 'list':
            # 모든 유저 조회: 매니저만
            return request.user.role == User.Role.MANAGER

        if getattr(view, 'action', None) in ['retrieve', 'update', 'partial_update']:
            return True  # object-level에서 한 번 더 체크
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            # 매니저는 아무나 조회 가능, 일반 유저는 본인만
            if request.user.role == User.Role.MANAGER:
                return True
            return obj.id == request.user.id

        if view.action in ['update', 'partial_update']:
            # 본인만 수정 가능 (매니저도 다른 사람 정보는 못 바꿈)
            return obj.id == request.user.id

        return False


class NotificationPermission(permissions.BasePermission):
    """
    NotificationViewSet 전용 권한:

    - 매니저(manager):
        - 모든 Notification CRUD 가능
    - 강사(instructor):
        - list/retrieve: 본인 소유 것만
        - mark_as_read: 본인 소유 것만
        - create/update/destroy 불가
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)

        if role == User.Role.MANAGER:
            # 매니저는 모든 action 허용
            return True

        if role == User.Role.INSTRUCTOR:
            # 강사는 읽기 및 mark_as_read 만 허용
            if getattr(view, 'action', None) in ['list', 'retrieve', 'mark_as_read']:
                return True
            # 일반 update/partial_update/destroy/create 안됨
            return False

        return False

    def has_object_permission(self, request, view, obj):
        role = getattr(request.user, 'role', None)

        if role == User.Role.MANAGER:
            return True

        if role == User.Role.INSTRUCTOR:
            # 본인 소유의 알림만
            return obj.user_id == request.user.id

        return False
