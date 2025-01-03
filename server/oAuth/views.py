from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, GroupSerializer, WeComConfigSerializer, FeiShuConfigSerializer, DingTalkConfigSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from .models import User, WeComConfig, FeiShuConfig, DingTalkConfig
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from note.models import NoteGroup  # 导入笔记分组模型
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action


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

class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集
    """
    queryset = User.objects.filter(is_superuser=False).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def check_admin(self):
        """检查当前用户是否是管理员"""
        if not self.request.user.role == 'admin' and not self.request.user.role == 'superuser':
            raise PermissionDenied("只有管理员可以执行此操作")
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

    def perform_create(self, serializer):
        # 保存用户
        user = serializer.save()

        # 更新用户时加密密码
        password = serializer.validated_data.get('password')
        if password:
            user.set_password(password)
        
        # 创建用户的默认笔记分组
        group_name = user.get_full_name()
        if not group_name:
            group_name = user.username
            
        note_group_instance = NoteGroup.objects.create(
            name=group_name,
            creator=user
        )
        note_group_instance.creator = user
        note_group_instance.save()
        user.note_group.add(note_group_instance)
    
    def perform_update(self, serializer):
        # 先保存一份请求数据的副本
        note_ids = None
        group_ids = None
        if 'note' in self.request.data or 'note_group' in self.request.data:
            self.check_admin()
            note_ids = self.request.data.get('note', [])
            group_ids = self.request.data.get('note_group', [])

        # 如果请求包含笔记或分组授权数据，检查管理员权限
        if 'note' in self.request.data or 'note_group' in self.request.data:
            self.check_admin()
            
        # 获取请求数据中的笔记和分组ID列表
        note_ids = self.request.data.get('note', [])
        group_ids = self.request.data.get('note_group', [])
            
        # 保存用户基本信息
        user = serializer.save()

        # 更新用户时加密密码
        password = serializer.validated_data.get('password')
        if password:
            user.set_password(password)
        
        # 更新笔记授权关系
        if note_ids is not None:
            user.note.clear()
            if note_ids:
                user.note.add(*note_ids)
        
        # 更新分组授权关系
        if group_ids is not None:
            user.note_group.clear()
            if group_ids:
                user.note_group.add(*group_ids)
        
        return user

class GroupViewSet(viewsets.ModelViewSet):
    """
    用户组管理视图集
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

class WeComConfigViewSet(viewsets.ModelViewSet):
    queryset = WeComConfig.objects.all()
    serializer_class = WeComConfigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.role in ['admin', 'superuser']:
            raise PermissionDenied("只有管理员可以管理配置")
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def current(self):
        """获取当前启用的配置"""
        config = WeComConfig.objects.filter(enabled=True).first()
        if config:
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        return Response(None)

class FeiShuConfigViewSet(viewsets.ModelViewSet):
    queryset = FeiShuConfig.objects.all()
    serializer_class = FeiShuConfigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.role in ['admin', 'superuser']:
            raise PermissionDenied("只有管理员可以管理配置")
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def current(self):
        """获取当前启用的配置"""
        config = FeiShuConfig.objects.filter(enabled=True).first()
        if config:
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        return Response(None)

class DingTalkConfigViewSet(viewsets.ModelViewSet):
    queryset = DingTalkConfig.objects.all()
    serializer_class = DingTalkConfigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.role in ['admin', 'superuser']:
            raise PermissionDenied("只有管理员可以管理配置")
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def current(self):
        """获取当前启用的配置"""
        config = DingTalkConfig.objects.filter(enabled=True).first()
        if config:
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        return Response(None)
