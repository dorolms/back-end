from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Lecture, LectureRecruitment, Application
from .serializers import (
    LectureSerializer,
    LectureRecruitmentSerializer,
    ApplicationSerializer,
)
from .permissions import (
    LecturePermission,
    LectureRecruitmentPermission,
    ApplicationPermission,
)

User = get_user_model()


class LectureViewSet(viewsets.ModelViewSet):
    """
    Lecture

    - (매니저) 조회/등록/수정/삭제
    - (강사) 조회만
    """
    queryset = Lecture.objects.select_related('manager').all()
    serializer_class = LectureSerializer
    permission_classes = [LecturePermission]

    def get_queryset(self):
        qs = super().get_queryset()

        # 간단 필터 예시 (선택사항)
        lecture_type = self.request.query_params.get('type')
        status = self.request.query_params.get('status')
        manager_id = self.request.query_params.get('manager_id')

        if lecture_type:
            qs = qs.filter(type=lecture_type)
        if status:
            qs = qs.filter(status=status)
        if manager_id:
            qs = qs.filter(manager_id=manager_id)

        return qs


class LectureRecruitmentViewSet(viewsets.ModelViewSet):
    """
    LectureRecruitment

    - (매니저) 조회/등록/수정/삭제
    - (강사) 조회만
    """
    queryset = LectureRecruitment.objects.select_related('lecture').all()
    serializer_class = LectureRecruitmentSerializer
    permission_classes = [LectureRecruitmentPermission]

    def get_queryset(self):
        qs = super().get_queryset()

        lecture_id = self.request.query_params.get('lecture_id')
        if lecture_id:
            qs = qs.filter(lecture_id=lecture_id)

        return qs


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Application

    - (매니저) 조회/수정만
    - (강사, 본인 것만) 조회/등록/수정/삭제
    """
    queryset = Application.objects.select_related('lecture', 'user').all()
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationPermission]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.role == User.Role.MANAGER:
            # 매니저는 전체 조회 + 필터 제공
            lecture_id = self.request.query_params.get('lecture_id')
            user_id = self.request.query_params.get('user_id')
            assignment_status = self.request.query_params.get('assignment_status')
            applied_role = self.request.query_params.get('applied_role')

            if lecture_id:
                qs = qs.filter(lecture_id=lecture_id)
            if user_id:
                qs = qs.filter(user_id=user_id)
            if assignment_status:
                qs = qs.filter(assignment_status=assignment_status)
            if applied_role:
                qs = qs.filter(applied_role=applied_role)

            return qs

        # 강사는 본인 지원 내역만
        if user.role == User.Role.INSTRUCTOR:
            return qs.filter(user=user)

        # 이외 역할은 permission 에서 걸러지긴 하지만, 안전하게 빈 쿼리셋
        return qs.none()

    def get_serializer_context(self):
        """
        serializer 에 request 전달 (ApplicationSerializer에서 사용)
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        """
        - 강사: 본인 user 로 Application 생성
        """
        user = self.request.user

        # 강사가 지원 시, snapshot 자동 저장
        if user.role == User.Role.INSTRUCTOR:
            portfolio_snapshot = user.portfolio_content or ''
            serializer.save(user=user, portfolio_snapshot=portfolio_snapshot)
        else:
            # 일반적으로는 permission 에서 막히지만, 방어적으로 작성
            serializer.save()
