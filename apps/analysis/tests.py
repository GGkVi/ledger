# from datetime import datetime
# from django.contrib.auth import get_user_model
# from apps.accounts.models import Accounts, BankCodes
# from apps.transactions.models import Transaction
#
# User = get_user_model()
#
# # 초기화 및 유저 생성
# user = User.objects.filter(username = "molly123")
# if not user:
#     user = User.objects.create_user(username="molly123", password="molly1234")
#     print("user created: molly123")
#
# # 계좌 + 은행 생성(계좌 입력용)
# account = Accounts.objects.filter(user = user)
# if not account:
#     bank = BankCodes.objects.get_or_create(code = "003", name = "IBK기업은행")
#     account = Accounts.objects.create(
#         user=user,
#         bank_code=bank,
#         account_number='123456789',
#         account_purpose="default",
#     )
#
# # 거래내역 (False: 지출) 얘는 원금. transaction 생성
# try:
#     Transaction.objects.create(
#         account_id=account,
#         amount=10000 * 10000,
#         category="원금",
#         is_deposit=True,
#        is_hidden=False,
#       created_at=datetime(2025, 1, 1, 12, 0, 0)
#     )
#     print("transaction: income created")
#
#     for i in range(7):
#         Transaction.objects.create(
#             account_id=account,
#             amount=72000 * ((i + 0.5) / 2),
#             category="식비",
#             is_deposit=False,
#             is_hidden=False,
#             created_at=datetime(2025, 1, 1 + i, 12, 0, 0)
#         )
#     print("transaction: outcome created")
#
# except Exception as e:
#     print(f"{e}: transaction creation failed")
#
# print("실행 완료")