from rest_framework import serializers

from .models import Analysis, Targets


class AnalysisSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = [
            "id",
            "target",
            "period",
            "period_start",
            "period_end",
            "description",
            "image_url",
            "download_url",
            "created_at",
        ]

    def get_image_url(self, obj):
        if obj.result_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.result_image.url)
            return obj.result_image.url
        return None

    def get_download_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/analysis/{obj.id}/download/")
        return f"/api/analysis/{obj.id}/download/"


class AnalysisCreateSerializer(serializers.Serializer):
    start_date = serializers.DateField(help_text="시작일: YYYY-MM-DD")
    end_date = serializers.DateField(help_text="종료일: YYYYY-MM-DD")
    target = serializers.ChoiceField(
        choices=Targets.choices,
        default=Targets.ALL,
        help_text="expense / income / all",
    )

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("시작일은 종료일보다 앞서야 합니다.")
        return data
