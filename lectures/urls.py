from django.urls import path
from .views import (
    LectureListView, LectureDetailView,
    LectureCalendarView, ApplicationCreateView, ApplicationListView,
)

urlpatterns = [
    path('', LectureListView.as_view(), name='lecture-list'),
    path('calendar/', LectureCalendarView.as_view(), name='lecture-calendar'),
    path('<int:pk>/', LectureDetailView.as_view(), name='lecture-detail'),
    path('<int:pk>/apply/', ApplicationCreateView.as_view(), name='lecture-apply'),
    path('<int:pk>/applications/', ApplicationListView.as_view(), name='lecture-applications'),
]
