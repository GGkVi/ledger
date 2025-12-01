from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


# 회원가입
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "phone", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        """
        password validation (Django 기본 패스워드 정책 적용)
        """
        try:
            validate_password(password=data["password"], user=User(**data))
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return data

    def create(self, validated_data):
        """
        비밀번호는 set_password로 해싱
        """
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            phone=validated_data["phone"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


# 로그인
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# 프로필 조회 / 수정
# delete는 views에서 처리하니까 지웠어요
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "phone", "created_at"]
        read_only_fields = ["email", "created_at"]

    def update(self, instance, validated_data):
        """
        username, phone만 수정 가능
        """
        instance.username = validated_data.get("username", instance.username)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance
