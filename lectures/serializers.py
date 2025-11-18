from rest_framework import serializers
from .models import Lecture, LectureRecruitment, Application

class LectureSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.name', read_only=True)
    class Meta:
        model = Lecture
        fields = [
            'id', 'title', 'type', 'category', 'status',
            'lecture_start_datetime', 'lecture_end_datetime',
            'location', 'manager', 'manager_name',
            'target_audience', 'content_description',
            'special_notes', 'attachment_url', 'created_at'
        ]

class LectureRecruitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureRecruitment
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Application
        fields = [
            'id', 'lecture', 'user', 'applicant_name',
            'applied_role', 'portfolio_snapshot',
            'assignment_status', 'assigned_role', 'applied_at'
        ]
