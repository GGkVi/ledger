from django.urls import path

from .views import TransactionDetailView, TransactionListCreateView

urlpatterns = [
    path("", TransactionListCreateView.as_view(), name="Transaction-list"),
    path("<int:pk>/", TransactionDetailView.as_view(), name="Transaction-detail"),
]


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
