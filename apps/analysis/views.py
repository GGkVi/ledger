from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .serializers import AnalysisCreateSerializer, AnalysisSerializer
from .analyzers import Analyzer
from .models import Analysis


class AnalysisView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return AnalysisCreateSerializer if self.request.method == "POST" else AnalysisSerializer

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]
        target = serializer.validated_data.get("target", "expense")

        analyzer = Analyzer(
            user=self.request.user,
            start_date=start_date,
            end_date=end_date,
            target=target,
        )

        return analyzer.run()


class AnalysisDetailView(generics.RetrieveAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user)


class AnalysisImageDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            analysis = Analysis.objects.get(pk=pk, user=request.user)
        except Analysis.DoesNotExist:
            return Response({"error": "분석 결과가 없습니다."}, status=404)

        image_path = os.path.join(settings.MEDIA_ROOT, str(analysis.result_image))

        if not os.path.exists(image_path):
            raise Http404("이미지 없음")

        response = FileResponse(open(image_path, "rb"), content_type="image/jpeg")
        response["Content-Disposition"] = (
            f'attachment; filename="analysis_{analysis.id}.jpeg"'
        )
        return response
