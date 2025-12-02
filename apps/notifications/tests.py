from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.analysis.models import Analysis
from apps.notifications.models import Notification
from apps.users.models import User


class NotificationAPITest(APITestCase):

    def setUp(self):
        # 유저 생성
        self.user = User.objects.create_user(
            email="test@example.com",
            username="tester",
            password="1234",
            phone="01012345678",
        )

        # JWT 인증
        refresh = RefreshToken.for_user(self.user)
        access = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        # Analysis 객체 하나 미리 생성 (choice 준수)
        self.analysis = Analysis.objects.create(
            user=self.user,
            target="expense",
            period="monthly",
            period_start="2025-01-01",
            period_end="2025-01-31",
            description="1월 분석",
        )

    # 1) 시그널 테스트
    def test_signal(self):
        """
        Analysis 생성 시 자동으로 Notification 생성되는지 확인
        """
        analysis = Analysis.objects.create(
            user=self.user,
            target="income",
            period="weekly",
            period_start="2025-02-01",
            period_end="2025-02-07",
            description="2월 분석",
        )

        self.assertEqual(Notification.objects.count(), 2)

        notif = Notification.objects.filter(analysis=analysis).first()

        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)
        self.assertEqual(notif.analysis, analysis)

    # 2) 읽지 않은 알림 조회 테스트
    def test_list_notifications(self):
        """
        GET 읽지 않은 알림만 조회
        """
        # unread: 1개 (시그널 생성)
        notif_unread = Notification.objects.get(analysis=self.analysis)

        # 읽은 알림 추가 (analysis 필수)
        Notification.objects.create(
            analysis=self.analysis, message="읽은 알림", is_read=True
        )

        response = self.client.get("/api/notifications/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # unread only
        self.assertEqual(response.data[0]["id"], notif_unread.id)

    # 3) 알림 읽음 처리 테스트
    def test_read_notification(self):
        """
        PATCH /api/notifications/<pk>/read/
        읽음 처리 후 is_read=True로 변경되었는지 확인
        """
        notif = Notification.objects.get(analysis=self.analysis)

        response = self.client.patch(f"/api/notifications/{notif.id}/read/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
