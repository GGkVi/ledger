from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionDetailSerializer, TransactionSerializer


class TransactionListCreateView(ListCreateAPIView):
    """
    GET: 거래 목록 조회 (필터링 가능)
    POST: 거래 생성 (balance_after 자동 계산)
    """

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # swagger에 필터 표시를 위한 GET 오버라이드
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "is_deposit",
                openapi.IN_QUERY,
                description="입금 여부 (true=입금 / false=출금)",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "min_amount",
                openapi.IN_QUERY,
                description="최소 금액",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "max_amount",
                openapi.IN_QUERY,
                description="최대 금액",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        operation_description="로그인한 사용자의 모든 거래 조회",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        qs = Transaction.objects.filter(
            is_hidden=False,
            account_id__user=user,
        ).order_by("-created_at")

        is_deposit = self.request.query_params.get("is_deposit")
        min_amount = self.request.query_params.get("min_amount")
        max_amount = self.request.query_params.get("max_amount")

        if is_deposit in ("true", "false"):
            qs = qs.filter(is_deposit=(is_deposit == "true"))

        if min_amount:
            qs = qs.filter(amount__gte=min_amount)

        if max_amount:
            qs = qs.filter(amount__lte=max_amount)

        return qs

    def perform_create(self, serializer):
        account = serializer.validated_data["account_id"]

        last_tx = (
            Transaction.objects.filter(account_id=account, is_hidden=False)
            .order_by("-created_at")
            .first()
        )
        previous_balance = last_tx.balance_after if last_tx else 0

        amount = serializer.validated_data["amount"]
        is_deposit = serializer.validated_data["is_deposit"]

        new_balance = (
            previous_balance + amount if is_deposit else previous_balance - amount
        )

        serializer.save(balance_after=new_balance)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET: 특정 거래 조회
    PUT/PATCH: 수정 + 이후 거래 재계산
    DELETE: soft delete + 이후 거래 재계산
    """

    serializer_class = TransactionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            is_hidden=False,
            account_id__user=user,
        ).order_by("-created_at")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        data.pop("is_hidden", None)

        previous_tx = (
            Transaction.objects.filter(
                account_id=instance.account_id,
                created_at__lt=instance.created_at,
                is_hidden=False,
            )
            .order_by("-created_at")
            .first()
        )
        previous_balance = previous_tx.balance_after if previous_tx else 0

        new_is_deposit = data.get("is_deposit", instance.is_deposit)
        new_amount = data.get("amount", instance.amount)

        new_balance = (
            previous_balance - int(new_amount)
            if not new_is_deposit
            else previous_balance + int(new_amount)
        )

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(balance_after=new_balance, updated_at=datetime.now())

        self._recalc_after_update(instance)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        account = instance.account_id
        created_at = instance.created_at

        instance.is_hidden = True
        instance.save(update_fields=["is_hidden"])

        self._recalc_after_delete(account, created_at)

        return Response(status=status.HTTP_204_NO_CONTENT)

    # ------ helper methods ------

    def _recalc_after_update(self, updated):
        after = Transaction.objects.filter(
            account_id=updated.account_id,
            created_at__gt=updated.created_at,
            is_hidden=False,
        ).order_by("created_at")

        current = updated.balance_after

        for tx in after:
            current = current + tx.amount if tx.is_deposit else current - tx.amount
            tx.balance_after = current
            tx.save(update_fields=["balance_after"])

    def _recalc_after_delete(self, account, created_at):
        previous_tx = (
            Transaction.objects.filter(
                account_id=account,
                created_at__lt=created_at,
                is_hidden=False,
            )
            .order_by("-created_at")
            .first()
        )

        current = previous_tx.balance_after if previous_tx else 0

        after = Transaction.objects.filter(
            account_id=account,
            created_at__gt=created_at,
            is_hidden=False,
        ).order_by("created_at")

        for tx in after:
            current = current + tx.amount if tx.is_deposit else current - tx.amount
            tx.balance_after = current
            tx.save(update_fields=["balance_after"])
