from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from oAuth.models import GitLabConfig, GitLabUser
from oAuth.serializers import UserSerializer
import requests

User = get_user_model()

class GitLabLoginView(APIView):
    """GitLab 登录视图"""
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            code = request.data.get('code')
            if not code:
                return Response({'message': '缺少 code 参数'}, status=status.HTTP_400_BAD_REQUEST)

            # 获取 GitLab 配置
            config = GitLabConfig.objects.filter(enabled=True).first()
            if not config:
                return Response({'message': 'GitLab 登录未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 构建 GitLab API 基础 URL
            gitlab_server = config.gitlab_server or 'https://gitlab.com'
            if gitlab_server.endswith('/'):
                gitlab_server = gitlab_server[:-1]

            # 获取访问令牌
            token_url = f'{gitlab_server}/oauth/token'
            token_data = {
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': config.redirect_uri
            }
            
            headers = {
                'Accept': 'application/json'
            }
            
            token_resp = requests.post(token_url, data=token_data, headers=headers)
            
            try:
                token_info = token_resp.json()
            except Exception as e:
                return Response({
                    'message': '解析 GitLab 响应失败',
                    'detail': str(e),
                    'response': token_resp.text
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            if 'error' in token_info:
                return Response({
                    'message': '获取 GitLab 令牌失败',
                    'error': token_info.get('error'),
                    'error_description': token_info.get('error_description')
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if 'access_token' not in token_info:
                return Response({'message': '获取 GitLab 令牌失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            access_token = token_info.get('access_token')
            
            # 获取用户信息
            user_url = f'{gitlab_server}/api/v4/user'
            headers = {'Authorization': f'Bearer {access_token}'}
            user_resp = requests.get(user_url, headers=headers)
            user_info = user_resp.json()

            if 'id' not in user_info:
                return Response({'message': '获取 GitLab 用户信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 提取用户数据
            gitlab_id = str(user_info.get('id'))
            name = user_info.get('name', '')
            username = user_info.get('username', '')
            email = user_info.get('email', '')
            avatar_url = user_info.get('avatar_url', '')

            gitlab_user_data = {
                'gitlab_id': gitlab_id,
                'name': name,
                'username': username,
                'email': email,
                'avatar_url': avatar_url
            }

            # 查找或创建本地用户
            gitlab_user_instance = GitLabUser.objects.update_or_create(
                gitlab_id=gitlab_id, 
                defaults=gitlab_user_data
            )

            user = gitlab_user_instance[0].user
            if not user:
                user_data = {
                    'username': f'gitlab_{gitlab_id}',
                    'first_name': name or username,
                    'email': email,
                    'avatar': avatar_url,
                    'is_active': True
                }
                user = User.objects.update_or_create(
                    username=f'gitlab_{gitlab_id}', 
                    defaults=user_data
                )[0]
                gitlab_user_instance[0].user = user
                gitlab_user_instance[0].save()
            else:
                user.avatar = avatar_url
                user.first_name = name or username
                if email:
                    user.email = email
                user.save()
            
            # 生成JWT令牌
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })

        except Exception as e:
            return Response({
                'message': '登录失败',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 