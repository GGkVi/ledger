from django.db import models


class Transaction(models.Model):
    # id는 장고가 자동으로 생성
    # account_id 값을 외래키로 받아옴
    account_id = models.ForeignKey(
        "accounts.Accounts",  # 또는 "Account"
        on_delete=models.CASCADE,
        related_name="transactions",
        db_column="account_id",
    )
    # 입/출금 구분용 불리언 값. False가 디폴트값. False=출금
    is_deposit = models.BooleanField(default=False)
    # 입/출금 값
    amount = models.BigIntegerField(default=0)
    # null과 blank 공식문서 https://django-orm-cookbook-ko.readthedocs.io/en/latest/null_vs_blank.html
    balance_after = models.BigIntegerField(default=0)
    # 거래내역 분류
    category = models.CharField(
        max_length=8,
        null=True,
        blank=True,
    )
    # 거래내역 상세메모
    content = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    # 숨김값 디폴트는 False
    is_hidden = models.BooleanField(default=False)
    # 생성시간, 업데이트 시간 단, 입출금값은 업데이트 불가로
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transaction"
