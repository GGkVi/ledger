from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction

        fields = "__all__"

        read_only_fields = [
            "id",
            "account_id",
            "is_hidden",
            "created_at",
            "updated_at",
        ]


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction

        fields = "__all__"

        read_only_fields = [
            "id",
            "account_id",
            "created_at",
        ]
