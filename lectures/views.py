from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Lecture, LectureRecruitment, Application
from .serializers import LectureSerializer, LectureRecruitmentSerializer, ApplicationSerializer

# 강의 달력 일정용 API
class LectureCalendarView(generics.ListAPIView):
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        qs = Lecture.objects.filter(lecture_start_datetime__isnull=False)
        if start and end:
            qs = qs.filter(lecture_start_datetime__gte=start, lecture_end_datetime__lte=end)
        return qs.select_related('manager')

# 강의 전체 목록 (필터링)
class LectureListView(generics.ListAPIView):
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Lecture.objects.select_related('manager')
        # 유형, 상태, 기간 등 프론트 요청 파라미터에 따라 필터링
        type = self.request.query_params.get('type')
        status_ = self.request.query_params.get('status')
        if type:
            qs = qs.filter(type=type)
        if status_:
            qs = qs.filter(status=status_)
        return qs

# 강의 상세정보 및 모집/지원 현황 포함 반환 (팝업에 활용)
class LectureDetailView(generics.RetrieveAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        lecture = self.get_object()
        recruitment = getattr(lecture, 'recruitment_info', None)
        recruitment_json = LectureRecruitmentSerializer(recruitment).data if recruitment else {}
        applications = Application.objects.filter(lecture=lecture)
        applications_json = ApplicationSerializer(applications, many=True).data
        base_data = LectureSerializer(lecture).data
        return Response({
            'lecture': base_data,
            'recruitment': recruitment_json,
            'applications': applications_json
        })

# 강의 지원 신청
class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 강의별 지원 내역(지원자 현황 등)
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lecture_id = self.kwargs.get('pk')
        return Application.objects.filter(lecture__id=lecture_id)
