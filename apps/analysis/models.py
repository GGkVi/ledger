from django.core.exceptions import ValidationError
from django.db import models


# enum용 클래스 선언: 총지출 금액 Enumerate. 총지출이라 Total 붙임
class Targets(models.TextChoices):
    EXPENSE = "expense", "총 지출"
    INCOME = "income", "총 수입"
    ALL = "all", "전체"


# Periods: 분석 단위(기간). 커스텀 기간 추가도 생각해 볼 것
class Periods(models.TextChoices):
    WEEKLY = "weekly", "주간"
    MONTHLY = "monthly", "월간"


class Analysis(models.Model):
    # id 비선언 → 자동생성
    # 유저id FK 받아오기
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="analyses",
        db_column="user_id",
        verbose_name="사용자",
    )

    # 분석 주제(지출, 수입). 필터링 자주 발생함 → 인덱스를 추가=추적하기 쉽게
    target = models.CharField(
        max_length=10,
        choices=Targets.choices,
        verbose_name="분석 대상",
        db_index=True,
    )

    # 분석 단위기간 (주간, 월간) 필터링 자주 발생함 → 인덱스추가 주간/월간 필터링용
    period = models.CharField(
        max_length=10,
        choices=Periods.choices,
        null=True,
        blank=True,
        verbose_name="분석 단위",
        db_index=True,
    )
    # 분석 기간 시작일/종료일 하단에 Validation 검증
    period_start = models.DateField(verbose_name="분석 시작일")
    period_end = models.DateField(verbose_name="분석 종료일")

    # 분석 결과 설명
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="분석 요약",
    )

    # 분석 이미지 파일 경로
    result_image = models.ImageField(
        upload_to="analysis/",
        null=True,
        blank=True,
        verbose_name="분석 그래프",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # validation 추가/(시작일 < 종료일 검증할 수 있게) clean으로 자동 호출+검증(by Django 컨벤션)
    def clean(self):
        super().clean()
        if self.period_start and self.period_end:
            if self.period_start > self.period_end:
                raise ValidationError(
                    {"ValidationError": "period end must be after period start."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    # ordering은 정렬 순서 지정. -앞에 붙이면 내림차순 = 최신순으로 정렬해 줌
    def __str__(self):
        return f"[{self.user.username}] {self.target} ({self.period or 'manual'})"

    class Meta:
        db_table = "analysis"
        verbose_name = "가계부 분석"
        verbose_name_plural = "가계부 분석 목록"

        ordering = ["-created_at"]
