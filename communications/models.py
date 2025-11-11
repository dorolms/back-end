from django.db import models
from django.conf import settings


#  Message
class Message(models.Model):
    # 발신자
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # 발신자가 탈퇴해도 메시지는 남음
        related_name='sent_messages',
        verbose_name='발신자',
        null=True
    )

    # 수신자
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # 수신자가 탈퇴해도 메시지는 남음
        related_name='received_messages',
        verbose_name='수신자',
        null=True
    )

    content = models.TextField('메시지 내용')

    sent_at = models.DateTimeField('발송 시각', auto_now_add=True)

    read_at = models.DateTimeField('수신 확인 시각', blank=True, null=True)

    class Meta:
        ordering = ['-sent_at']  # 최신 순
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
            models.Index(fields=['sender', 'recipient']),
        ]

    def __str__(self):
        sender_name = self.sender.name if self.sender else '알 수 없음'
        recipient_name = self.recipient.name if self.recipient else '알 수 없음'
        return f"{sender_name} -> {recipient_name} ({self.content[:20]}...)"