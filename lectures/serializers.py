from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Lecture, LectureRecruitment, Application

User = get_user_model()


class LectureSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.name', read_only=True)

    class Meta:
        model = Lecture
        fields = [
            'id',
            'title',
            'type',
            'category',
            'status',
            'lecture_start_datetime',
            'lecture_end_datetime',
            'location',
            'manager',
            'manager_name',
            'target_audience',
            'content_description',
            'special_notes',
            'attachment_url',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class LectureRecruitmentSerializer(serializers.ModelSerializer):
    lecture_title = serializers.CharField(source='lecture.title', read_only=True)

    class Meta:
        model = LectureRecruitment
        fields = [
            'lecture',
            'lecture_title',
            'application_start_date',
            'application_end_date',
            'max_participants',
            'recruitment_main_needed',
            'recruitment_assist_needed',
            'fee_main',
            'fee_assist',
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    lecture_title = serializers.CharField(source='lecture.title', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'lecture',
            'lecture_title',
            'user',
            'user_name',
            'applied_role',
            'portfolio_snapshot',
            'assignment_status',
            'assigned_role',
            'applied_at',
        ]
        read_only_fields = ['id', 'applied_at', 'user']

    def validate(self, attrs):
        """
        - 강사는 assignment_status / assigned_role 을 수정할 수 없도록 제한
        - unique_together(lecture, user, applied_role) 체크
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        # 강사 수정 제한
        if request and user and getattr(user, 'role', None) == User.Role.INSTRUCTOR:
            forbidden_fields = {}
            for field in ['assignment_status', 'assigned_role']:
                if field in attrs:
                    forbidden_fields[field] = '강사는 이 값을 수정할 수 없습니다.'
            if forbidden_fields:
                raise serializers.ValidationError(forbidden_fields)

        # unique_together 체크 (생성 시)
        if not self.instance:
            lecture = attrs.get('lecture')
            applied_role = attrs.get('applied_role')
            # user 는 create 시 perform_create 에서 request.user 로 세팅
            if request and user and lecture and applied_role:
                exists = Application.objects.filter(
                    lecture=lecture,
                    user=user,
                    applied_role=applied_role,
                ).exists()
                if exists:
                    raise serializers.ValidationError(
                        '이미 해당 강의에 동일한 역할로 지원한 내역이 있습니다.'
                    )

        return attrs
