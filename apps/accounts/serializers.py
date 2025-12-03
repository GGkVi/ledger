from rest_framework import serializers

from .models import Accounts


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ["id", "bank_code", "account_number", "account_purpose", "created_at"]
        read_only_fields = ["id", "created_at"]


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ["id", "bank_code", "account_number", "account_purpose", "created_at"]
        read_only_fields = fields  # 모든 필드를 읽기 전용으로 설정
