from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class LecturePermission(permissions.BasePermission):
    """
    LectureViewSet 전용

    - list/retrieve : 매니저, 강사 모두 허용
    - create/update/partial_update/destroy : 매니저만
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)
        action = getattr(view, 'action', None)

        if action in ['list', 'retrieve']:
            return role in [User.Role.MANAGER, User.Role.INSTRUCTOR]

        # 그 외(생성/수정/삭제)는 매니저만
        return role == User.Role.MANAGER

    def has_object_permission(self, request, view, obj):
        # 객체 단위에서도 동일한 정책 적용
        return self.has_permission(request, view)


class LectureRecruitmentPermission(permissions.BasePermission):
    """
    LectureRecruitmentViewSet 전용

    - list/retrieve : 매니저, 강사 모두 허용
    - create/update/partial_update/destroy : 매니저만
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)
        action = getattr(view, 'action', None)

        if action in ['list', 'retrieve']:
            return role in [User.Role.MANAGER, User.Role.INSTRUCTOR]

        return role == User.Role.MANAGER

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ApplicationPermission(permissions.BasePermission):
    """
    ApplicationViewSet 전용

    - 매니저(manager):
        - list/retrieve/update/partial_update 허용
        - create/destroy 불가
    - 강사(instructor):
        - list/retrieve: 본인 지원 내역만
        - create: 본인 지원만
        - update/partial_update/destroy: 본인 지원 내역만
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)
        action = getattr(view, 'action', None)

        # 강사/매니저 외에는 접근 불가
        if role not in [User.Role.MANAGER, User.Role.INSTRUCTOR]:
            return False

        # 매니저 권한
        if role == User.Role.MANAGER:
            # 매니저는 create/destroy 불가
            if action in ['create', 'destroy']:
                return False
            return True

        # 강사 권한
        if role == User.Role.INSTRUCTOR:
            # 강사는 모든 action 정의 (list, retrieve, create, update, partial_update, destroy) 허용
            # 단, 객체 레벨에서 본인 소유인지 체크
            return True

        return False

    def has_object_permission(self, request, view, obj):
        role = getattr(request.user, 'role', None)
        action = getattr(view, 'action', None)

        if role == User.Role.MANAGER:
            # 매니저는 조회 및 수정 가능, 삭제는 has_permission 에서 이미 막힘
            return True

        if role == User.Role.INSTRUCTOR:
            # 강사는 본인 지원 내역만 조회/수정/삭제 가능
            return obj.user_id == request.user.id

        return False
