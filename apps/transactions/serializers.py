from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    거래 생성 및 목록 조회용 Serializer
    - 계좌(account_id)는 필수
    - amount, is_deposit, category, content 입력 가능
    """

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account_id",
            "is_deposit",
            "amount",
            "balance_after",
            "category",
            "content",
            "is_hidden",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "balance_after",
            "created_at",
            "updated_at",
            "is_hidden",
        ]


class TransactionDetailSerializer(serializers.ModelSerializer):
    """
    단일 조회 / 수정 Serializer
    업데이트 시 amount, is_deposit, category, content만 변경 가능
    """

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account_id",
            "is_deposit",
            "amount",
            "balance_after",
            "category",
            "content",
            "is_hidden",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "account_id",
            "balance_after",
            "is_hidden",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """
        수정할 때 필요한 유효성 검사
        """
        amount = attrs.get("amount")
        if amount is not None and amount <= 0:
            raise serializers.ValidationError("금액(amount)은 1원 이상이어야 합니다.")

        return attrs
