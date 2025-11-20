from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Notification

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    회원가입용 Serializer
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'name',
            'phone_number',
            'role',
            'profile_photo_url',
            'bio',
            'portfolio_content',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    User 조회/수정용 Serializer
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',
            'phone_number',
            'role',
            'profile_photo_url',
            'bio',
            'portfolio_content',
        ]
        # 이메일/역할/아이디/username 수정 불가 예시
        read_only_fields = ['id', 'username', 'role', 'email']


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification Serializer
    """
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'user_name',
            'lecture',
            'message',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
