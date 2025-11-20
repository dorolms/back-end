from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LectureViewSet,
    LectureRecruitmentViewSet,
    ApplicationViewSet,
)

router = DefaultRouter()
router.register(r'lectures', LectureViewSet, basename='lecture')
router.register(r'recruitments', LectureRecruitmentViewSet, basename='lecture-recruitment')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
