import os

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from django.conf import settings

from apps.analysis.models import Analysis
from apps.transactions.models import Transaction

# 한글 폰트 설정
font_candidates = ["NanumGothic", "NanumBarunGothic", "Malgun Gothic", "AppleGothic"]
available_fonts = [f.name for f in font_manager.fontManager.ttflist]
for f in font_candidates:
    if f in available_fonts:
        plt.rcParams["font.family"] = f
        break
plt.rcParams["axes.unicode_minus"] = False


class Analyzer:
    """
    소비 분석기 (입금/출금/전체)
    """

    def __init__(self, user, start_date, end_date, target="expense", period="custom"):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date
        self.target = target
        self.period = period

    # 1. 거래 조회
    def _get_transactions(self):
        qs = Transaction.objects.filter(
            account_id__user=self.user,
            is_hidden=False,
            created_at__date__range=(self.start_date, self.end_date),
        )

        # target에 따라 필터링
        if self.target == "income":
            qs = qs.filter(is_deposit=True)

        elif self.target == "expense":
            qs = qs.filter(is_deposit=False)

        # all이면 필터링 없음

        if not qs.exists():
            raise ValueError("해당 기간 거래내역이 없습니다.")

        return qs

    # 2. 데이터프레임 생성
    def _df(self, qs):
        df = pd.DataFrame(
            list(qs.values("amount", "is_deposit", "category", "created_at"))
        )

        df["date"] = pd.to_datetime(df["created_at"]).dt.date
        df["category"] = df["category"].fillna("기타")

        # signed_amount: 입금(+) / 출금(-)
        df["signed_amount"] = df.apply(
            lambda row: row["amount"] if row["is_deposit"] else -row["amount"], axis=1
        )

        return df

    # 3. 그래프 생성
    def _visualize(self, df):
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f"{self.start_date} ~ {self.end_date} 소비 분석", fontsize=17)

        # 1) 날짜별 +/-
        daily = df.groupby("date")["signed_amount"].sum()
        axes[0].bar(daily.index.astype(str), daily.values)
        axes[0].set_title("일자별 순지출(+수입 / -지출)")

        # 2) 카테고리별 지출(출금만)
        expense_df = df[df["signed_amount"] < 0]
        if not expense_df.empty:
            cat = expense_df.groupby("category")["signed_amount"].sum().abs()
            axes[1].pie(cat.values, labels=cat.index, autopct="%1.1f%%")
            axes[1].set_title("카테고리별 지출 비중")

        plt.tight_layout()

        # 저장 경로
        filename = (
            f"analysis/user_{self.user.id}/{self.start_date}_{self.end_date}.jpeg"
        )
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        plt.savefig(filepath, format="jpeg", dpi=100, bbox_inches="tight")
        plt.close()
        return filename

    # 4. 설명문 자동 생성
    def _description(self, df):
        income = int(df[df["is_deposit"]]["amount"].sum())
        expense = int(df[~df["is_deposit"]]["amount"].sum())
        net = income - expense

        top_category = (
            df[~df["is_deposit"]]
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        top_name = top_category.index[0] if not top_category.empty else "없음"

        return (
            f"{self.start_date} ~ {self.end_date} 분석 결과\n"
            f"총 수입: {income:,}원\n"
            f"총 지출: {expense:,}원\n"
            f"순소비: {net:,}원\n"
            f"최대 지출 카테고리: {top_name}"
        )

    # 5. 전체 실행
    def run(self):
        qs = self._get_transactions()
        df = self._df(qs)

        image_path = self._visualize(df)
        description = self._description(df)

        analysis = Analysis.objects.create(
            user=self.user,
            target=self.target,
            period=None,
            period_start=self.start_date,
            period_end=self.end_date,
            result_image=image_path,
            description=description,
        )
        return analysis
