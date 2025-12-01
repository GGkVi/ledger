from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


# 유저 권한
class Role(models.TextChoices):
    USER = "user", "사용자"
    ADMIN = "admin", "관리자"
    SUPERUSER = "superuser", "슈퍼유저"


# 유저 생성 유효성 검사
class UserManager(BaseUserManager):
    def create_user(self, email, username, password, phone):
        if not email:
            raise ValueError("올바른 이메일을 입력하세요")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )
        user.set_password(password)  # 비밀번호 해싱
        user.role = Role.USER  # 유저 권한
        user.is_active = True  # 활성화 상태
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, phone):
        user = self.create_user(email, username, password, phone)
        user.role = Role.SUPERUSER
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_admin(self, email, username, password, phone):
        user = self.create_user(email, username, password, phone)
        user.role = Role.ADMIN
        user.is_active = True
        user.save(using=self._db)
        return user


# 커스텀 유저 모델
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="이메일", unique=True)  # 이메일
    username = models.CharField(max_length=32)  # 유저 이름 & 닉네임
    password = models.CharField(max_length=255)  # 비밀번호
    phone = models.CharField(max_length=16)  # 전화번호
    is_active = models.BooleanField(default=True)  # 활성화 상태
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name="권한",
    )  # 유저 권한
    created_at = models.DateTimeField(auto_now_add=True)  # 생성된 날짜
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 날짜

    objects = UserManager()  # 유저 매니저 설정
    USERNAME_FIELD = "email"  # 식별자 필드
    EMAIL_FIELD = "email"  # 이메일 필드
    REQUIRED_FIELDS = ["username", "phone"]  # 필수 필드

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def get_full_name(self):  # 영어 이름
        return self.username

    def get_short_name(self):
        return self.username

    def get_username(self):
        return self.username

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.role in [Role.ADMIN, Role.SUPERUSER]

    @property
    def is_superuser(self):
        return self.role == Role.SUPERUSER

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def soft_delete(self):
        self.is_active = False
        self.save()


# blacklist token 테이블
class BlacklistToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blacklist_tokens"
    )
    token = models.CharField(max_length=500)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "블랙리스트 토큰"
        verbose_name_plural = "블랙리스트 토큰"

    def is_expired(self):
        return self.expires_at < timezone.now()  # 만료 시간 체크

    def __str__(self):
        return self.token
