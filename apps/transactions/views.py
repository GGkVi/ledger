from datetime import datetime

from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionDetailSerializer, TransactionSerializer


# C, R
class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 숨김값이랑 계좌id값으로 필터링 후 생성순 정렬 후 반환
        return Transaction.objects.filter(
            # 숨김 제외
            is_hidden=False,
            # 사용자 계정에 속한 거래만
            account_id__user=user,
        ).order_by("-created_at")

    def perform_create(self, serializer):
        account = serializer.validated_data["account_id"]

        last_transaction = (
            Transaction.objects.filter(account_id=account)
            .order_by("-created_at")
            .first()
        )
        previous_balance = last_transaction.balance_after if last_transaction else 0

        amount = serializer.validated_data.get("amount")
        is_deposit = serializer.validated_data.get("is_deposit")

        if not is_deposit:
            new_balance_after = previous_balance - amount
        else:
            new_balance_after = previous_balance + amount

        # transaction 저장
        serializer.save(balance_after=new_balance_after)


# U, D
class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            is_hidden=False,
            account_id__user=user,
        ).order_by("-created_at")

    def update(self, request, *args, **kwargs):
        # 값 입력받음
        instance = self.get_object()
        data = request.data.copy()
        updated_at = datetime.now()

        # 같은 계좌에서 입력받은 생성일 값보다 작은 것들 중 최근 거래내역
        previous_transaction = (
            Transaction.objects.filter(
                account_id=instance.account_id,
                created_at__lt=instance.created_at,
                is_hidden=False,
            )
            .order_by("-created_at")
            .first()
        )
        previous_balance = (
            previous_transaction.balance_after if previous_transaction else 0
        )

        new_is_deposit = data.get("is_deposit", instance.is_deposit)
        new_amount = data.get("amount", instance.amount)

        if not new_is_deposit:
            new_balance_after = previous_balance - new_amount
        else:
            new_balance_after = previous_balance + new_amount

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(balance_after=new_balance_after, updated_at=updated_at)
        ######
        after_transactions = Transaction.objects.filter(
            account_id=instance.account_id,
            created_at__gt=instance.created_at,
            is_hidden=False,
        ).order_by(
            "created_at"
        )  # 과거->미래 순으로 계산

        current_balance = new_balance_after
        for i in after_transactions:
            if not i.is_deposit:
                current_balance -= i.amount
            else:
                current_balance += i.amount
            i.balance_after = current_balance
            i.save(update_fields=["balance_after"])

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # 삭제할 데이터 값 임시로 저장
        instance = self.get_object()
        account = instance.account_id
        created_at = instance.created_at

        # 기존 데이터 삭제
        self.perform_destroy(instance)

        # 삭제된 거래 이후 거래들 가져오기
        after_transactions = Transaction.objects.filter(
            account_id=account,
            created_at__gt=created_at,
            is_hidden=False,
        ).order_by(
            "created_at"
        )  # 과거 -> 미래 순으로

        # 삭제된 거래 이전의 마지막 balance_after 가져오기
        previous_transaction = (
            Transaction.objects.filter(
                account_id=account,
                created_at__lt=created_at,
                is_hidden=False,
            )
            .order_by("-created_at")
            .first()
        )

        new_balance = previous_transaction.balance_after if previous_transaction else 0

        # 이후 거래들 balance 재계산
        for i in after_transactions:
            if i.is_deposit:
                new_balance += i.amount
            else:
                new_balance -= i.amount
            i.balance_after = new_balance
            i.save(update_fields=["balance_after"])

        return Response()
