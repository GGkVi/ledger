import matplotlib
import pandas
from django.http import FileResponse, Http404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

matplotlib.use('Agg')
import os

import matplotlib.pyplot as plt
from django.conf import settings
from .serializers import AnalysisCreateSerializer, AnalysisSerializer

from apps.analysis.models import Analysis
from apps.transactions.models import Transaction

import matplotlib.font_manager as font_manager

# 한글 테스트용 폰트 설정
try:
    # 폰트 지정
    font_list = ['NanumGothic', 'NanumBarunGothic', 'Malgun Gothic', 'AppleGothic']
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]

    for font_name in font_list:
        if font_name in available_fonts:
            plt.rcParams['font.family'] = font_name
            break
    else:
        print("Warning: Korean font not found. Korean characters may not display correctly.")
        plt.rcParams['font.family'] = 'DejaVu Sans'

    # 마이너스는 수정
    plt.rcParams['axes.unicode_minus'] = False
except Exception as e:
    print(f"Font configuration warning: {e}")

"""
1. AnalysisListCreateView
  - GET : 목록 조회
  - POST : 생성
2. AnalysisDetailView
  - GET : 상세 조회
3. AnalysisImageDownloadView
  - GET : 파일 다운로드
"""

class AnalysisDetailView(generics.RetrieveAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user)

class AnalysisImageDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Analysis 조회
            analysis = Analysis.objects.get(pk=pk, user=request.user)

            # 이미지 파일 경로
            image_path = os.path.join(
                settings.MEDIA_ROOT,
                str(analysis.result_image)
            )

            if not os.path.exists(image_path):
                raise Http404("Image does not exist")

            response = FileResponse(
                open(image_path, 'rb'),
                content_type = 'image/jpeg'
            )

            filename = f"analysis_{analysis.period_start}_{analysis.period_end}.jpg"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        except Analysis.DoesNotExist:
            return Response(
                {"error" : "분석 결과를 찾을 수 없습니다."},
                status = status.HTTP_404_NOT_FOUND
            )


"""
AnalysisView (명칭이 이거 아닌거같긴한데 일단은 이걸로)
  - GET : 목록 조회 (get_queryset)
  - POST : 생성
"""
class AnalysisView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnalysisCreateSerializer
        return AnalysisSerializer

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']


        # 거래내역 존재 검증
        transactions = self._transaction_check(self.request.user, start_date, end_date)

        # DataFrame 생성
        df = self._create_dataframe(transactions)

        # 시각화 + 이미지 저장
        image_path = self._visualize(df, self.request.user, start_date, end_date)

        # 설명 생성
        description = self._generate_description(df, start_date, end_date)

        # Analysis 모델 저장
        serializer.save(
            user=self.request.user,
            target='expense',
            period='custom',
            period_start=start_date,
            period_end=end_date,
            result_image = image_path,
            description = description,
        )

    # 거래내역 조회해 주는 메서드, 구type 현is_deposit False: 지출만. is_hidden이 아닌 것만.
    def _transaction_check(self, user, start_date, end_date):
        transactions = Transaction.objects.filter(
            account_id__user=user,
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            is_deposit = False,
            is_hidden = False,
        )

        if not transactions.exists():
            raise ValidationError("Transaction does not exist")

        return transactions

    # dataframe 생성
    # try - except 구조 적용
    # 현재 category 내에 넣을 내용이 없음. 보완책 생각해 보겠음

    def _create_dataframe(self, transactions):
        data = list(transactions.values(
            'amount', 'category', 'created_at'
        ))

        # df는 d데이터f프레임 이란뜻
        df = pandas.DataFrame(data)

        # 날짜 컬럼 추가
        df['date'] = pandas.to_datetime(df['created_at']).dt.date

        # 카테고리 처리 (우선은 이렇게)
        df['category'] = df['category'].fillna('Null')

        return df

    def _visualize(self, df, user, start_date, end_date):

        fig, axes = plt.subplots(2, 1, figsize = (12, 10))
        fig.suptitle(
            f'가계부 분석 ({start_date} to {end_date})',
            fontsize = 16
        )

        # 상단 - 일별 지출 막대그래프
        self._chart_daily_bar(axes[0], df)

        # 하단 - 카테고리별 파이 차트(구현 되려나)
        self._chart_category_pie(axes[1], df)

        plt.tight_layout()

        # 파일 경로 생성
        filename = self._generate_filename(user, start_date, end_date)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # 이미지 저장(JPEG)
        plt.savefig(filepath, format='jpeg',dpi=100,bbox_inches='tight')
        plt.close()

        return filename

    # 일별 지출 막대 그래프
    def _chart_daily_bar(self, ax, df):
        daily = df.groupby('date')['amount'].sum().sort_index()
        dates_str = [d.strftime('%m/%d') for d in daily.index]
        amounts = daily.values

        bars = ax.bar(dates_str, amounts)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{int(height):,}원',
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight="bold"
            )

        # 평균선
        average = amounts.mean()
        ax.axhline(y=average, color='gray', linestyle='--', linewidth=2, label=f'평균: {int(average):,}원')

    # 기간 동안의 카테고리별 파이 차트
    def _chart_category_pie(self, ax, df):
        category = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        # 색상 팔레트
        colors = [
            '#FF6B6B',  # red
            '#4ECDC4',  # 도자기색
            '#45B7D1',  # skyblue
            '#FFA07A',  # salmon-red
            '#98D8C8',  # mint-green
            '#F7DC6F',  # yellow
            '#BB8FCE',  # purple
            '#85C1E2',  # blue
        ]

        # 파이 차트
        ax.pie(
            category.values,
            labels=category.index,
            colors=colors[:len(category)],
            shadow=True,
        )

        # 범례(legend)
        ax.set_title('항목별 지출 비중')
        legend_labels = [
            f'{category}: {int(amounts):,}원'
            for category, amounts in category.items()
        ]
        ax.legend(
            legend_labels,
            loc='center left',
            fontsize=10,
            fontweight="bold",
        )
    # 파일명 생성하는 메서드
    def _generate_filename(self, user, start_date, end_date):
        timestamp = pandas.Timestamp.now().strftime('%m%d_%H%M%S')
        return f"analysis/user_{user.id}/{start_date}_{end_date}_{timestamp}.jpeg"

    # 설명 생성하는 메서드
    def _generate_description(self, df, start_date, end_date):
        total = int(df['amount'].sum())
        daily_avg = int(df.groupby('date')['amount'].sum().mean())
        top_category = df.groupby('category')['amount'].sum().idxmax()

        return(
            f"FROM {start_date} TO {end_date}\n"
            f"총 지출: {total:,}원\n"
            f"일 평균: {daily_avg:,}원\n"
            f"최다 항목: {top_category}"
        )
