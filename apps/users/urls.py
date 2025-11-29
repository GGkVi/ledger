from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from .views import SignUpAPIView, LogoutAPIView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    # jwt views
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify"),
]
