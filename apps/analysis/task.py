from datetime import date, timedelta
from celery import shared_task
from django.contrib.auth import get_user_model

from .analyzers import Analyzer
from .models import Targets, Periods

User = get_user_model()


@shared_task
def create_weekly_expense_analysis(user_id):
    user = User.objects.get(id=user_id)
    end = date.today()
    start = end - timedelta(days=6)

    Analyzer(
        user=user,
        start_date=start,
        end_date=end,
        target=Targets.EXPENSE,
        period=Periods.WEEKLY,  # 스케줄링 분석
    ).run()


@shared_task
def create_monthly_expense_analysis(user_id):
    user = User.objects.get(id=user_id)
    end = date.today()
    start = end.replace(day=1)

    Analyzer(
        user=user,
        start_date=start,
        end_date=end,
        target=Targets.EXPENSE,
        period=Periods.MONTHLY,
    ).run()
