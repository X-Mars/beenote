from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from oAuth.models import GoogleConfig, GoogleUser
from oAuth.serializers import UserSerializer
import requests

User = get_user_model()

class GoogleLoginView(APIView):
    """Google登录视图"""
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            code = request.data.get('code')
            if not code:
                return Response({'message': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)

            # 获取Google配置
            config = GoogleConfig.objects.filter(enabled=True).first()
            if not config:
                return Response({'message': 'Google登录未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 获取访问令牌
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'code': code,
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'redirect_uri': config.redirect_uri,
                'grant_type': 'authorization_code'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
            token_resp = requests.post(token_url, data=token_data, headers=headers)
            
            try:
                token_info = token_resp.json()
            except Exception as e:
                return Response({
                    'message': '解析Google响应失败',
                    'detail': str(e),
                    'response': token_resp.text
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if 'error' in token_info:
                return Response({
                    'message': '获取Google令牌失败',
                    'error': token_info.get('error'),
                    'error_description': token_info.get('error_description')
                }, status=status.HTTP_400_BAD_REQUEST)

            if 'access_token' not in token_info:
                return Response({'message': '获取Google令牌失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            access_token = token_info.get('access_token')

            # 获取用户信息
            user_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}
            user_resp = requests.get(user_url, headers=headers)
            user_info = user_resp.json()

            if 'id' not in user_info:
                return Response({'message': '获取Google用户信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            google_id = user_info.get('id')
            email = user_info.get('email')
            name = user_info.get('name')
            picture = user_info.get('picture')
            given_name = user_info.get('given_name')
            family_name = user_info.get('family_name')

            google_user_data = {
                'google_id': google_id,
                'name': name,
                'email': email,
                'picture': picture,
                'given_name': given_name,
                'family_name': family_name
            }

            # 查找或创建本地用户
            google_user_instance = GoogleUser.objects.update_or_create(google_id=google_id, defaults=google_user_data)

            user = google_user_instance[0].user
            if not user:
                user_data = {
                    'username': google_id,
                    'first_name': name,
                    'email': email,
                    'avatar': picture,
                    'is_active': True
                }
                user = User.objects.update_or_create(username=google_id, defaults=user_data)[0]
                google_user_instance[0].user = user
                google_user_instance[0].save()
            else:
                user.avatar = picture
                user.first_name = name
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