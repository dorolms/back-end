from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# User 테이블
class User(AbstractUser):
    # 사용자 역할
    class Role(models.TextChoices):
        MANAGER = 'manager', '매니저'
        INSTRUCTOR = 'instructor', '강사'

    email = models.EmailField('이메일', unique=True, max_length=255)
    name = models.CharField('사용자 이름', max_length=100)
    phone_number = models.CharField('연락처', max_length=20, blank=True, null=True)
    role = models.CharField(
        '사용자 역할',
        max_length=20,
        choices=Role.choices,
        default=Role.INSTRUCTOR
    )
    profile_photo_url = models.URLField(
        '프로필 사진 URL',
        max_length=255,
        blank=True,
        null=True
    )
    bio = models.TextField('강사 이력 (소개)', blank=True, null=True)
    portfolio_content = models.TextField('포트폴리오 상세 내용', blank=True, null=True)
    first_name = None
    last_name = None

    def __str__(self):
        return f"[{self.get_role_display()}] {self.name} ({self.username})"


# Notification
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='알림 수신자'
    )

    lecture = models.ForeignKey(
        'lectures.Lecture',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='관련 강의'
    )

    message = models.TextField('알림 내용')
    is_read = models.BooleanField('읽음 여부', default=False)
    created_at = models.DateTimeField('알림 생성 시각', auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # 최신 순
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        # user 모델 인스턴스
        return f"[{self.user.name}님] {self.message[:20]}..."