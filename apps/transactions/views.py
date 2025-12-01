from datetime import datetime

from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionDetailSerializer, TransactionSerializer


# C, R
class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # R
    def get_queryset(self):
        account_id = self.request.query_params.get("account_id")
        return Transaction.objects.filter(
            is_hidden=False,  # 숨김 제외
            account_id=account_id,  # 사용자 계정에 속한 거래만
        ).order_by("-created_at")

    # C
    def perform_create(self, serializer):
        account_id = self.request.data.get("account_id")

        last_transaction = (
            Transaction.objects.filter(account_id=account_id)
            .order_by("-created_at")
            .first()
        )
        previous_balance = last_transaction.balance_after
        amount = serializer.validated_data.get("amount")
        is_deposit = serializer.validated_data.get("is_deposit")

        if not is_deposit:
            amount = -amount

        new_balance_after = previous_balance + amount

        serializer.save(account_id_id=account_id, balance_after=new_balance_after)


# U, D
class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get("account_id")
        return Transaction.objects.filter(
            account_id=account_id,  # 사용자 계정에 속한 거래만
        ).order_by("-created_at")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        category = request.data.get("category", None)
        content = request.data.get("content", None)
        is_hidden = request.data.get("is_hidden", None)
        updated_at = datetime.now()

        if category is not None:
            instance.category = category
        if content is not None:
            instance.content = content
        if is_hidden is not None:
            instance.is_hidden = is_hidden
        instance.updated_at = updated_at

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # 삭제할 대상 가져오기
        instance.delete()

        amount = instance.amount
        is_deposit = instance.is_deposit
        if not is_deposit:
            amount = -amount
        balance_after = instance.balance_after + amount

        instance.save(balance_after=balance_after)

        return Response({"message": "삭제되었습니다."})
