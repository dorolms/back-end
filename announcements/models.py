from django.db import models
from django.conf import settings


class Announcement(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='announcements',
        verbose_name='작성자',
        null=True,
        limit_choices_to={'role': 'manager'}
    )

    title = models.CharField('공지 제목', max_length=255)

    content = models.TextField('공지 내용')

    created_at = models.DateTimeField('작성일', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # 최신글을 맨 위로

    def __str__(self):
        return self.title