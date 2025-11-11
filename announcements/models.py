from django.db import models
from django.conf import settings


# Announcement
class Announcement(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # 작성자가 탈퇴해도 공지사항은 남음
        related_name='announcements',
        verbose_name='작성자(매니저)',
        blank=True,
        null=True,
        # 매니저만 작성 가능
        limit_choices_to={'role': 'manager'}
    )

    title = models.CharField('공지사항 제목', max_length=255)
    content = models.TextField('공지사항 내용')

    created_at = models.DateTimeField('작성일', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # 최신 순
        indexes = [
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title