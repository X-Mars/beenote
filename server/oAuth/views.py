from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from .models import User
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # 验证用户
            user = authenticate(request, username=username, password=password)
            
            if not user:
                return Response({
                    'message': '用户名或密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
            if not user.is_active:
                return Response({
                    'message': '用户已被禁用'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # 更新最后登录时间
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # 生成 JWT token
            refresh = RefreshToken.for_user(user)
            
            # 准备用户数据
            user_data = UserSerializer(user).data
            
            # 返回登录成功的响应
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data
            })
            
        except Exception as e:
            return Response({
                'message': '服务器错误',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_stats(request):
    try:
        today = timezone.now().date()
        active_users = User.objects.filter(
            last_active_at__date=today
        ).count()
        
        total_users = User.objects.count()
        
        return Response({
            'active_users': active_users,
            'total_users': total_users
        })
    except Exception as e:
        return Response({
            'message': '获取统计数据失败',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'message': '获取用户信息失败',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
