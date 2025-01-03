from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from oAuth.models import DingTalkConfig, DingTalkUser
from oAuth.serializers import UserSerializer
import requests
import time
import hmac
import base64
import hashlib
import urllib.parse

User = get_user_model()

class DingTalkLoginView(APIView):
    """钉钉登录视图"""
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            authCode = request.data.get('authCode')
            if not authCode:
                return Response({'message': '缺少authCode参数'}, status=status.HTTP_400_BAD_REQUEST)

            # 获取钉钉配置
            config = DingTalkConfig.objects.filter(enabled=True).first()
            if not config:
                return Response({'message': '钉钉登录未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 获取访问令牌
            token_url = 'https://api.dingtalk.com/v1.0/oauth2/userAccessToken'
            get_token_data = {
                'clientId': config.client_id,
                'clientSecret': config.client_secret,
                'grantType': 'authorization_code',
                'code': authCode,
            }
            token_resp = requests.post(token_url, json=get_token_data)
            token_data = token_resp.json()
            
            if 'accessToken' not in token_data:
                return Response({'message': '获取钉钉令牌失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            access_token = token_data.get('accessToken')

            # 获取用户信息
            user_url = 'https://api.dingtalk.com//v1.0/contact/users/me'

            header = {
                'x-acs-dingtalk-access-token': access_token
            }

            user_resp = requests.get(url=user_url, headers=header)
            user_info = user_resp.json()

            if 'openId' not in user_info:
                return Response({'message': '获取钉钉用户信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            mobile = user_info.get('mobile')
            name = user_info.get('nick')
            open_id = user_info.get('openId')
            avatar = user_info.get('avatarUrl')

            dingtalk_user_data = {
                'open_id': open_id,
                'union_id': user_info.get('unionId'),
                'name': name,
                'avatar': user_info.get('avatarUrl'),
                'mobile': mobile
            }

            # 查找或创建本地用户
            dingtalk_user_instance = DingTalkUser.objects.update_or_create(open_id=open_id, defaults=dingtalk_user_data)

            user = dingtalk_user_instance[0].user
            if not user:
                user_data = {
                    'username': open_id,
                    'first_name': name,
                    'avatar': avatar,
                    'is_active': True
                }
                user = User.objects.update_or_create(username=open_id, defaults=user_data)[0]
                dingtalk_user_instance[0].user = user
                dingtalk_user_instance[0].save()
            else:
                user.avatar = avatar
                user.first_name = name
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

    def get_signature(self, timestamp: str, app_secret: str) -> str:
        """生成钉钉签名"""
        message = f"{timestamp}\n{app_secret}"
        hmac_code = hmac.new(
            app_secret.encode('utf-8'),
            message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return urllib.parse.quote_plus(base64.b64encode(hmac_code))
