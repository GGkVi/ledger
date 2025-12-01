from django.contrib import admin
from django.utils.html import format_html
from .models import Analysis

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'target',
        'period',
        'period_start',
        'period_end',
        'created_at',
    ]

# 필터
list_filter = [
    'target',  # 지출/수입
    'period',  # 주간/월간
    'created_at',  # 생성일
]

# 검색
search_fields = [
    'user__username'
    'user__email',
    'description',
]

# 기본 정렬 (최신순)
ordering = ['-created_at']

# 페이지당 항목 수
list_per_page = 20

# 이미지 미리보기 메서드
@admin.display(description='그래프 미리보기')
def image_preview(self, obj):
    if obj.result_image:
        return format_html(
            '<a href="{}" target="_blank">'
            '<img src="{}" style="max-width:100px; max-height:100px; border-radius:5px;"/>'
            '</a>',
            obj.result_image.url,
            obj.result_image.url
        )
    return '-'