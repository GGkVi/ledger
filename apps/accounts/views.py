from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Accounts
from .serializers import AccountDetailSerializer, AccountSerializer


class AccountListCreateView(generics.ListCreateAPIView):
    """
    GET: 로그인한 유저의 계좌 목록 조회
    POST: 새로운 계좌 생성
    """

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 유저의 계좌만 조회
        return Accounts.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 계좌 생성 시 user 필드는 request.user로 자동 설정
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: 특정 계좌 조회
    DELETE: 특정 계좌 삭제
    PATCH/PUT: 수정 불가
    """

    serializer_class = AccountDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 본인 계좌만 조회 가능
        return Accounts.objects.filter(user=self.request.user)

    # 수정 금지 (crd만 제공)
    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "계좌 정보는 생성 후 수정할 수 없습니다."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "계좌 정보는 생성 후 수정할 수 없습니다."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
