# from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import SignUpSerializer, UserSerializer   
from rest_framework.permissions import IsAuthenticated, AllowAny 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions 
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BlacklistToken
from datetime import datetime

# 회원가입 
class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny] # 모든 사용자 접근 허용
    authentication_classes = [] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# 로그아웃
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            BlacklistToken.objects.create(
                user=request.user,
                token=str(refresh_token),
                expires_at=datetime.fromtimestamp(token["exp"]),
            )
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to logout"}, status=status.HTTP_400_BAD_REQUEST)

# 유저 조회
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs): # 유저 프로필 조회 
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 유저 수정
class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs): 
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 유저 삭제
class UserProfileDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.soft_delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)