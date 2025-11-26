from django.conf import settings
from django.db import models


class BankCodes(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="은행 코드")
    name = models.CharField(max_length=50, verbose_name="은행 이름")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = "bank_codes"
        verbose_name = "은행코드"
        verbose_name_plural = "은행 코드 목록"
        ordering = ["code"]


class Accounts(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
        verbose_name="계좌 소유자",
    )

    bank_code = models.ForeignKey(
        BankCodes,
        on_delete=models.PROTECT,
        related_name="accounts",
        verbose_name="은행 코드",
    )

    account_number = models.CharField(
        max_length=30, unique=True, verbose_name="계좌번호"
    )
    account_purpose = models.CharField(
        max_length=50, verbose_name="계좌 용도(생활비/저축/투자 등)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} ({self.bank_code.name})"

    class Meta:
        db_table = "accounts"
        verbose_name = "계좌"
        verbose_name_plural = "계좌목록"
        ordering = ["-created_at"]
