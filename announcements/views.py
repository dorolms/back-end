from rest_framework import generics, permissions
from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementMiniSerializer


class IsManagerWriteOrAuthenticatedRead(permissions.BasePermission):

    def has_permission(self, request, view):
        # 로그인이 안 되어 있으면 거부
        if not request.user or not request.user.is_authenticated:
            return False

        # GET, HEAD, OPTIONS는 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # POST, PUT, DELETE는 'manager'일 때만 허용
        return request.user.role == 'manager'


# 목록 조회 및 생성 (/api/announcements/)
class AnnouncementListCreateView(generics.ListCreateAPIView):
    """
    GET: 공지사항 목록 조회 (최신순)
    POST: 공지사항 생성 (매니저 전용)
    """
    queryset = Announcement.objects.all().order_by('-created_at')  # 최신글이 위로 오게 정렬
    serializer_class = AnnouncementSerializer
    permission_classes = [IsManagerWriteOrAuthenticatedRead]

    def perform_create(self, serializer):
        # POST 요청 시 호출됨
        # author 필드를 self.request.user로 채워서 저장
        serializer.save(author=self.request.user)


# /api/announcements/<int:pk>/
class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: 공지사항 상세 조회
    PUT: 공지사항 수정 (매니저 전용, 제목/내용만 수정됨)
    DELETE: 공지사항 삭제 (매니저 전용)
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsManagerWriteOrAuthenticatedRead]


# /announcements/recent/
class RecentAnnouncementListView(generics.ListAPIView):
    """
    GET: 최신 공지사항 5개의 제목과 날짜만 조회
    """
    # 최신순 5개
    queryset = Announcement.objects.all().order_by('-created_at')[:5]
    serializer_class = AnnouncementMiniSerializer

    permission_classes = [IsManagerWriteOrAuthenticatedRead]