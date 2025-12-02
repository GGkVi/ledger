from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    GET 로그인 유저의 읽지 않은 알림 조회
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # 분석(analysis)의 user가 현재 유저고, 읽지 않은 알림만
        return Notification.objects.filter(
            analysis__user=user,
            is_read=False,
        ).order_by("-created_at")


class NotificationReadView(generics.UpdateAPIView):
    """
    PUT/PATCH 알림 읽음 처리 (is_read = True)
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        notification = self.get_object()

        analysis = notification.analysis
        # 본인 데이터인지 확인
        if analysis is None or analysis.user != request.user:
            return Response(
                {"detail": "읽을 수 없는 알림입니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(NotificationSerializer(notification).data)
