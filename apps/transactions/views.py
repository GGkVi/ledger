from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from .models import Transaction
from .serializers import TransactionSerializer


# C, R
class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # R
    # def get_queryset(self):
    #     # 쿼리 파라미터로 계좌id 값 받음
    #     account_id = self.request.query_params.get("account_id")
    #     # 숨김값이랑 계좌id값으로 필터링 후 생성순 정렬 후 반환
    #     return Transaction.objects.filter(
    #         # 숨김 제외
    #         is_hidden=False,
    #         # 사용자 계정에 속한 거래만
    #         account_id=account_id,
    #     ).order_by("-created_at")

    def get_queryset(self):
        user = self.request.user
        # 숨김값이랑 계좌id값으로 필터링 후 생성순 정렬 후 반환
        return Transaction.objects.filter(
            # 숨김 제외
            is_hidden=False,
            # 사용자 계정에 속한 거래만
            account_id__user=user,
        ).order_by("-created_at")

    # C
    # def perform_create(self, serializer):
    #     account_id = self.request.data.get("account_id")
    #
    #     last_transaction = (
    #         Transaction.objects.filter(account_id=account_id)
    #         .order_by("-created_at")
    #         .first()
    #     )
    #     previous_balance = last_transaction.balance_after if last_transaction else 0
    #     amount = serializer.validated_data.get("amount")
    #     is_deposit = serializer.validated_data.get("is_deposit")
    #
    #     if not is_deposit:
    #         amount = -amount
    #
    #     new_balance_after = previous_balance + amount
    #
    #     serializer.save(account_id_id=account_id, balance_after=new_balance_after)
    #


# # U, D
# class TransactionDetailView(RetrieveUpdateDestroyAPIView):
#     serializer_class = TransactionDetailSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         account_id = self.request.query_params.get("account_id")
#         # 사용자 계정에 속한 거래만 조회
#         return Transaction.objects.filter(
#             account_id=account_id,
#         ).order_by("-created_at")
#
#     def update(self, request, *args, **kwargs):
#         # 값 입력받음
#         instance = self.get_object()
#         data = request.data.copy()
#         # 같은 계좌에서 입력받은 생성일 값보다 작은 것들 중 최근 거래내역
#         previous_transaction = (
#             Transaction.objects.filter(
#                 account_id=instance.account_id,
#                 created_at__lt=instance.created_at,
#             )
#             .order_by("-created_at")
#             .first()
#         )
#         previous_balance = previous_transaction.balance_after
#         new_is_deposit = data["is_deposit"]
#         new_amount = data["amount"]
#         if not new_is_deposit:
#             new_amount = -new_amount
#         data["balance_after"] = previous_balance + new_amount
#
#         serializer = self.get_serializer(instance, data=data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#
#     # 수정할 계좌 아이디 최근 거래내역 불러오기
#     account_id = self.request.data.get("account_id")
#     last_transaction = (
#         Transaction.objects.filter(account_id=account_id)
#         .order_by("-created_at")
#         .first()
#     )
#     # 잔액 가져오기
#     previous_balance_after = last_transaction.balance_after
#     # 요청값 불러오기
#     is_deposit = request.data.get("is_deposit")
#     amount = request.data.get("amount")
#     category = request.data.get("category", None)
#     content = request.data.get("content", None)
#     updated_at = datetime.now()
#     # 출금이면 금액 음수로 바꾸기
#     if not is_deposit:
#         amount = -amount
#     # 잔액 계산
#     balance_after = previous_balance_after + previous_amount + amount
#     # 인스턴스에 값 집어넣기
#     if is_deposit is not None:
#         instance.is_deposit = is_deposit
#     if amount is not None:
#         instance.amount = amount
#     if balance_after is not None:
#         instance.balance_after = balance_after
#     if category is not None:
#         instance.category = category
#     if content is not None:
#         instance.content = content
#     instance.updated_at = updated_at
#
#     instance.save()
#
# def delete(self, request, *args, **kwargs):
#     # 삭제할 값 숨김처리(소프트 삭제)
#     instance = self.get_object()
#     instance.is_hidden = True
#     instance.save()
#
#
