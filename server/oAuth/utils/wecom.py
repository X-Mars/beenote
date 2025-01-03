from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from oAuth.models import WeComConfig, WeComUser
from oAuth.serializers import UserSerializer
import requests
import json

User = get_user_model()

class WeComLoginView(APIView):
    """企业微信登录视图"""
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'message': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取企业微信配置
        config = WeComConfig.objects.filter(enabled=True).first()
        if not config:
            return Response({'message': '企业微信登录未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 获取访问令牌
        token_url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={config.corp_id}&corpsecret={config.secret}'
        token_resp = requests.get(token_url)
        token_data = token_resp.json()

        if token_data.get('errcode') != 0:
            return Response({'message': '获取企业微信令牌失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        access_token = token_data.get('access_token')

        # 获取用户信息
        user_url = f'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={access_token}&code={code}'
        user_resp = requests.get(user_url)
        user_info = user_resp.json()

        if user_info.get('errcode') != 0:
            return Response({'message': '获取企业微信用户信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        user_id = user_info.get('UserId')
        avatar = user_info.get('avatar')

        # 获取用户详细信息
        detail_url = f'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={access_token}&userid={user_id}'
        detail_resp = requests.get(detail_url)
        detail_data = detail_resp.json()

        if detail_data.get('errcode') != 0:
            return Response({'message': '获取企业微信用户详细信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        wecom_user_data = {
            'wecom_user_id': user_id,
            'name': detail_data.get('name'),
            'avatar': avatar,
            'mobile': detail_data.get('mobile'),
            'email': detail_data.get('email'),
            'position': detail_data.get('position')
        }
        wecom_user_instance = WeComUser.objects.update_or_create(wecom_user_id=user_id, defaults=wecom_user_data)
        user = wecom_user_instance[0].user
        if not user:
            user_data = {
                'username': user_id,
                'first_name': detail_data.get('name', ''),
                'avatar': avatar,
                'is_active': True
            }
            user = User.objects.update_or_create(username=user_id, defaults=user_data)[0]
            wecom_user_instance[0].user = user
            wecom_user_instance[0].save()
        else:
            user.avatar = avatar
            user.first_name = detail_data.get('name', '')
            user.save()

        # 生成JWT令牌
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
