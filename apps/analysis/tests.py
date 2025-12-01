from datetime import date, datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Analysis
from .views import AnalysisView
from apps.transactions.models import Transaction
from apps.accounts.models import Accounts, BankCodes

User = get_user_model()

class SimpleAnalysisTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'Molly',
            password = 'molly1234',
        )

        self.bank = BankCodes.objects.create(
            code = '003',
            name = 'IBK기업은행',
        )

        self.account = Accounts.objects.create(
            user = self.user,
            bank_code = self.bank,
            account_number = '123456789',
            account_purpose = "default",
        )

        # 거래내역 (False: 지출) 얘는 원금
        # is_deposit이 아니라 type 아니었나? 언제바꼈지;
        Transaction.objects.create(
            account_id = self.account,
            amount = 10000 * 10000,
            category = "원금",
            is_deposit = True,
            is_hidden = False,
            created_at = datetime(2025, 1, 1, 12, 0, 0)
        )
        
        for i in range(7):
            Transaction.objects.create(
                account_id = self.account,
                amount = 72000 * (i+1),
                category = "저녁",
                is_deposit = False,
                is_hidden= False,
                created_at = datetime(2025, 1, i + 1, 12, 0, 0)
            )

    def test_create_analysis(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post('/api/analysis/', {
            'start_date' : '2025-01-01',
            'end_date' : '2025-01-07'
        }, format = 'json')

        print(f"\n 응답 코드: {response.status_code}")
        print(f"분석 개수: {Analysis.objects.count()}")

        if response.status_code == 201:
            try:
                analysis = Analysis.objects.first()
                print(f"이미지 생성: {bool(analysis.result_image)}")
                print(f"설명: {analysis.description[:30]}" if analysis.description else "설명 읎음")
            except Analysis.DoesNotExist:
                print("status code is good, problem with something inside?")
        else:
            print(f"에러: {response.data}")