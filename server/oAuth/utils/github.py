from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from oAuth.models import GitHubConfig, GitHubUser
from oAuth.serializers import UserSerializer
import requests

User = get_user_model()

class GitHubLoginView(APIView):
    """GitHub登录视图"""
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            code = request.data.get('code')
            if not code:
                return Response({'message': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)

            # 获取GitHub配置
            config = GitHubConfig.objects.filter(enabled=True).first()
            if not config:
                return Response({'message': 'GitHub登录未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 获取访问令牌
            token_url = 'https://github.com/login/oauth/access_token'
            token_resp = requests.post(token_url, data={
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'code': code,
                'redirect_uri': config.redirect_uri
            }, headers={'Accept': 'application/json'})
            
            token_data = token_resp.json()
            access_token = token_data.get('access_token')
            
            if not access_token:
                return Response({'message': '获取GitHub令牌失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 获取用户信息
            user_url = 'https://api.github.com/user'
            user_resp = requests.get(
                user_url,
                headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/json'
                }
            )
            user_info = user_resp.json()

            if 'id' not in user_info:
                return Response({'message': '获取GitHub用户信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 获取用户邮箱
            email_url = 'https://api.github.com/user/emails'
            email_resp = requests.get(
                email_url,
                headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/json'
                }
            )
            email_data = email_resp.json()
            primary_email = next((email['email'] for email in email_data if email['primary']), None)

            github_user_data = {
                'github_id': str(user_info['id']),
                'login': user_info['login'],
                'name': user_info['name'],
                'bio': user_info['bio'],
                'email': primary_email or user_info.get('email'),
                'avatar_url': user_info['avatar_url'],
                'location': user_info['location']
            }

            # 查找或创建本地用户
            github_user_instance = GitHubUser.objects.update_or_create(
                github_id=github_user_data['github_id'],
                defaults=github_user_data
            )

            user = github_user_instance[0].user
            if not user:
                user_data = {
                    'username': github_user_data['github_id'],
                    'first_name': github_user_data['name'] or '',
                    'email': github_user_data['email'],
                    'avatar': github_user_data['avatar_url'],
                    'is_active': True
                }
                user = User.objects.update_or_create(
                    username=user_data['username'],
                    defaults=user_data
                )[0]
                github_user_instance[0].user = user
                github_user_instance[0].save()
            else:
                user.avatar = github_user_data['avatar_url']
                user.first_name = github_user_data['name'] or ''
                user.email = github_user_data['email'] or user.email
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