from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    LogoutAPIView,
    SignUpAPIView,
    UserProfileAPIView,
    UserProfileDeleteAPIView,
    UserProfileUpdateAPIView,
)

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),  # 회원가입
    path("logout/", LogoutAPIView.as_view(), name="logout"),  # 로그아웃
    path("profile/", UserProfileAPIView.as_view(), name="profile"),  # 유저 조회
    path(
        "profile/update/", UserProfileUpdateAPIView.as_view(), name="profile-update"
    ),  # 유저 수정
    path(
        "profile/delete/", UserProfileDeleteAPIView.as_view(), name="profile-delete"
    ),  # 유저 삭제
    # jwt views
    path("token/", TokenObtainPairView.as_view(), name="login"),  # 로그인
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),  # 토큰 갱신
    path("token/verify/", TokenVerifyView.as_view(), name="verify"),  # 토큰 검증
]
