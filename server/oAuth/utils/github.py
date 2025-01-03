#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from ..models import GitHubConfig, GitHubUser, User
from ..serializers import UserSerializer

class GitHubLoginView(APIView):
    """GitHub OAuth登录视图"""
    permission_classes = []
    authentication_classes = []

    def get_github_config(self):
        """获取启用的GitHub配置"""
        return GitHubConfig.objects.filter(enabled=True).first()

    def get_access_token(self, code, config):
        """获取GitHub访问令牌"""
        try:
            response = requests.post(
                'https://github.com/login/oauth/access_token',
                data={
                    'client_id': config.client_id,
                    'client_secret': config.client_secret,
                    'code': code,
                    'redirect_uri': config.redirect_uri
                },
                headers={'Accept': 'application/json'}
            )
            response.raise_for_status()
            return response.json().get('access_token')
        except Exception as e:
            print(f'获取GitHub访问令牌失败: {str(e)}')
            return None

    def get_user_info(self, access_token):
        """获取GitHub用户信息"""
        try:
            response = requests.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/json'
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'获取GitHub用户信息失败: {str(e)}')
            return None

    def create_or_update_user(self, github_info, access_token):
        """创建或更新用户"""
        github_id = str(github_info['id'])
        
        # 查找现有的GitHub用户
        github_user = GitHubUser.objects.filter(github_id=github_id).first()
        
        if github_user:
            # 更新现有用户信息
            github_user.name = github_info.get('name')
            github_user.email = github_info.get('email')
            github_user.avatar_url = github_info.get('avatar_url')
            github_user.access_token = access_token
            github_user.save()
            return github_user.user
        
        # 创建新用户
        username = f"github_{github_id}"
        email = github_info.get('email', f"{username}@github.com")
        
        # 创建Django用户
        user = User.objects.create(
            username=username,
            email=email,
            first_name=github_info.get('name', ''),
            avatar=github_info.get('avatar_url'),
            is_active=True
        )
        
        # 创建GitHub用户信息
        GitHubUser.objects.create(
            user=user,
            github_id=github_id,
            login=github_info['login'],
            name=github_info.get('name'),
            email=github_info.get('email'),
            avatar_url=github_info.get('avatar_url'),
            access_token=access_token
        )
        
        return user

    def get(self, request):
        """处理GitHub回调"""
        code = request.GET.get('code')
        if not code:
            return Response({
                'detail': '缺少必要的code参数'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取GitHub配置
        config = self.get_github_config()
        if not config:
            return Response({
                'detail': 'GitHub登录未配置'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 获取访问令牌
        access_token = self.get_access_token(code, config)
        if not access_token:
            return Response({
                'detail': '获取GitHub访问令牌失败'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取用户信息
        github_info = self.get_user_info(access_token)
        if not github_info:
            return Response({
                'detail': '获取GitHub用户信息失败'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建或更新用户
        user = self.create_or_update_user(github_info, access_token)
        
        # 生成JWT令牌
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }) 