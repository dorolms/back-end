from django.urls import path
from .views import AnnouncementListCreateView, RecentAnnouncementListView, AnnouncementDetailView

urlpatterns = [
    # 목록 GET, POST
    # /api/announcements/
    path('', AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    # 최신 공지 5개 GET
    # /api/announcements/recent/
    path('recent/', RecentAnnouncementListView.as_view(), name='announcement-recent'),
    # 상세 GET, PUT, DELETE
    # /api/announcements/1/
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
]