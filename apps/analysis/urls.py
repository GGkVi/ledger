from django.urls import path

from .views import AnalysisDetailView, AnalysisImageDownloadView, AnalysisView

app_name = "analysis"

urlpatterns = [
    # 생성 & 목록
    path("", AnalysisView.as_view(), name="analysis-list-create"),
    # 상세 조회
    path("<int:pk>/", AnalysisDetailView.as_view(), name="analysis-detail"),
    # 이미지 다운로드
    path(
        "<int:pk>/download/",
        AnalysisImageDownloadView.as_view(),
        name="analysis-download",
    ),
]

# AnalysisView(generics.ListAPIView):
# AnalysisImageDownloadView():
# AnalysisDetailView(generics.RetrieveUpdateAPIView):
