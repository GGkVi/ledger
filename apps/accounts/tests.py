from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Accounts, BankCodes
from apps.users.models import User


class AccountsAPITest(APITestCase):
    """
    Accounts API (CRD) 기능 테스트
    - Create
    - Read (list, detail)
    - Update 잘 막혔는지 보기
    - Delete
    """

    def setUp(self):
        """
        공통 초기 데이터 생성
        """
        # 테스트용 사용자 생성
        self.user = User.objects.create_user(
            email="test@example.com",
            username="tester",
            password="1234",
            phone="01012345678",
        )

        # JWT 토큰 인증 헤더 설정
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
        )

        # 계좌 생성 시 필요 은행코드
        self.bank, _ = BankCodes.objects.get_or_create(code="090", name="카카오뱅크")

        # accounts/ URL
        self.list_url = reverse("account-list")

    def test_create_account(self):
        """
        POST: 계좌 생성
        """
        data = {
            "bank_code": self.bank.id,
            "account_number": "123-4567-8900",
            "account_purpose": "생활비",
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(response.data["account_number"], "123-4567-8900")

    def test_list_accounts(self):
        """
        GET: 계좌 목록 조회
        """
        # 테스트용 계좌 생성 (2개)
        Accounts.objects.create(
            user=self.user,
            bank_code=self.bank,
            account_number="00-1111",
            account_purpose="저축",
        )
        Accounts.objects.create(
            user=self.user,
            bank_code=self.bank,
            account_number="00-2222",
            account_purpose="생활비",
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_account(self):
        """
        GET: 단일 계좌 조회
        """
        acc = Accounts.objects.create(
            user=self.user,
            bank_code=self.bank,
            account_number="12-3456",
            account_purpose="월세",
        )

        url = reverse("account-detail", kwargs={"pk": acc.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_number"], "12-3456")

    def test_update_not_allowed(self):
        """
        PUT: 수정 불가 확인
        """
        acc = Accounts.objects.create(
            user=self.user,
            bank_code=self.bank,
            account_number="77-8888",
            account_purpose="여행",
        )

        url = reverse("account-detail", kwargs={"pk": acc.id})
        update_data = {
            "bank_code": self.bank.id,
            "account_number": "99-9999",
            "account_purpose": "수정됨",
        }

        response = self.client.put(url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_not_allowed(self):
        """
        PATCH: 부분 수정 불가 확인
        """
        acc = Accounts.objects.create(
            user=self.user,
            bank_code=self.bank,
            account_number="12-9999",
            account_purpose="기타",
        )

        url = reverse("account-detail", kwargs={"pk": acc.id})
        response = self.client.patch(url, {"account_purpose": "변경"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_account(self):
        """
        DELETE: 계좌 삭제
        """
        acc = Accounts.objects.create(
            user=self.user,
            bank_code=self.bank,
            account_number="22-3333",
            account_purpose="비상금",
        )

        url = reverse("account-detail", kwargs={"pk": acc.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Accounts.objects.filter(id=acc.id).exists())
