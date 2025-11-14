from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    # 작성자 이름 (자동)
    author_name = serializers.CharField(source='author.name', read_only=True)

    # 작성일 (자동&포맷 지정)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id',
            'author_name',
            'title',
            'content',
            'created_at',
        ]

        # title과 content만 보내는 값이고, 나머지는 알아서 처리
        read_only_fields = ['author_name', 'created_at']


class AnnouncementMiniSerializer(serializers.ModelSerializer):
    """
    매니저 홈페이지 전용 최신 목록
    """
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id',
            'title',
            'created_at',
        ]