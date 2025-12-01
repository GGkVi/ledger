from rest_framework import serializers

from apps.accounts.models import Accounts

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(queryset=Accounts.objects.all())

    class Meta:
        model = Transaction

        fields = "__all__"

        read_only_fields = [
            "id",
            "balance_after",
            "is_hidden",
            "created_at",
            "updated_at",
        ]


class TransactionDetailSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(queryset=Accounts.objects.all())

    class Meta:
        model = Transaction

        fields = "__all__"

        read_only_fields = [
            "id",
            "balance_after",
            "is_hidden",
            "created_at",
            "updated_at",
        ]
