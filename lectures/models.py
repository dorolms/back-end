from django.db import models
from django.conf import settings


# Lecture
class Lecture(models.Model):
    class LectureType(models.TextChoices):
        GENERAL = 'general', '일반 (노랑)'
        COMPETITION = 'competition', '대회 (하늘)'
        CAMP = 'camp', '캠프 (연두)'
        DOROLAND = 'doroland', '도로랜드 (파랑)'
        BOOTH = 'booth', '부스 (핑크)'
        ETC = 'etc', '기타 (회색)'

    class LectureStatus(models.TextChoices):
        RECRUITING = 'recruiting', '모집중'
        ALLOCATING = 'allocating', '배정 중'
        COMPLETED = 'completed', '배정 완료'

    title = models.CharField('강의명', max_length=255)

    type = models.CharField(
        '강의 유형',
        max_length=20,
        choices=LectureType.choices,
        blank=True,
        null=True
    )

    category = models.CharField('강의 구분', max_length=50, blank=True, null=True)

    status = models.CharField(
        '강의 상태',
        max_length=20,
        choices=LectureStatus.choices,
        default=LectureStatus.RECRUITING
    )

    lecture_start_datetime = models.DateTimeField('강의 시작 일시', blank=True, null=True)
    lecture_end_datetime = models.DateTimeField('강의 종료 일시', blank=True, null=True)

    location = models.CharField('강의 장소', max_length=255, blank=True, null=True)

    # 담당 매니저
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # 매니저가 탈퇴해도 강의는 남음
        related_name='managed_lectures',
        verbose_name='담당 매니저',
        blank=True,
        null=True,
        # 매니저만 선택 가능
        limit_choices_to={'role': 'manager'}
    )

    target_audience = models.CharField('교육 대상', max_length=100, blank=True, null=True)
    content_description = models.TextField('콘텐츠 설명', blank=True, null=True)
    special_notes = models.TextField('특이사항', max_length=1000, blank=True, null=True)
    attachment_url = models.URLField('첨부파일 URL', max_length=255, blank=True, null=True)

    created_at = models.DateTimeField('생성일', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # 최신 순
        indexes = [
            models.Index(fields=['manager']),
            models.Index(fields=['status']),
            models.Index(fields=['type']),
            models.Index(fields=['lecture_start_datetime']),
        ]

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title}"


# LectureRecruitment
class LectureRecruitment(models.Model):
    lecture = models.OneToOneField(
        Lecture,
        on_delete=models.CASCADE,  # 강의가 삭제되면 모집 정보도 삭제
        primary_key=True,
        related_name='recruitment_info',
        verbose_name='강의'
    )

    application_start_date = models.DateField('강사 모집 시작일', blank=True, null=True)
    application_end_date = models.DateField('강사 모집 마감일', blank=True, null=True)

    max_participants = models.IntegerField('모집 인원', blank=True, null=True)
    recruitment_main_needed = models.IntegerField('필요한 주강사 수', default=0)
    recruitment_assist_needed = models.IntegerField('필요한 보조강사 수', default=0)

    fee_main = models.IntegerField('주강사 강의료', blank=True, null=True)
    fee_assist = models.IntegerField('보조강사 강의료', blank=True, null=True)

    def __str__(self):
        return f"{self.lecture.title} - 모집 정보"


# Application
class Application(models.Model):
    class LectureRole(models.TextChoices):
        MAIN = 'main', '주도로맨 (주강사)'
        ASSIST = 'assist', '보조도로맨 (보조강사)'

    class AssignmentStatus(models.TextChoices):
        PENDING = 'pending', '미배정'
        ASSIGNED = 'assigned', '배정완료'
        REJECTED = 'rejected', '배정 실패'

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,  # 강의가 삭제되면 지원 내역도 삭제
        related_name='applications',
        verbose_name='지원 강의'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 유저가 탈퇴하면 지원 내역도 삭제
        related_name='applications',
        verbose_name='지원 강사',
        # 강사만 지원 가능하도록
        limit_choices_to={'role': 'instructor'}
    )

    applied_role = models.CharField(
        '지원 역할',
        max_length=10,
        choices=LectureRole.choices
    )

    portfolio_snapshot = models.TextField(
        '지원 시점 포트폴리오',
        blank=True,
        null=True,
        help_text="지원 시점의 user.portfolio_content를 복사하여 저장"
    )

    assignment_status = models.CharField(
        '배정 상태',
        max_length=10,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.PENDING
    )

    assigned_role = models.CharField(
        '최종 배정된 역할',
        max_length=10,
        choices=LectureRole.choices,
        blank=True,
        null=True  # 미배정 상태일 수 있음
    )

    applied_at = models.DateTimeField('지원 일시', auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']
        # 강의 ID, 유저 ID, 지원 역할 unique
        unique_together = ('lecture', 'user', 'applied_role')
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.name} 님의 {self.lecture.title} 지원 ({self.get_applied_role_display()})"