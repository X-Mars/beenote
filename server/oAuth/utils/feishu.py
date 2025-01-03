from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from oAuth.models import FeiShuConfig, FeiShuUser
from oAuth.serializers import UserSerializer
import requests

User = get_user_model()

class FeiShuLoginView(APIView):
    """飞书登录视图"""
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            code = request.data.get('code')
            if not code:
                return Response({'message': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)

            # 获取飞书配置
            config = FeiShuConfig.objects.filter(enabled=True).first()
            if not config:
                return Response({'message': '飞书登录未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 获取访问令牌
            token_url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
            token_resp = requests.post(token_url, json={
                'app_id': config.app_id,
                'app_secret': config.app_secret
            })
            token_data = token_resp.json()
            
            if token_data.get('code') != 0:
                return Response({'message': '获取飞书令牌失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            access_token = token_data.get('tenant_access_token')

            # 获取用户信息
            user_url = 'https://open.feishu.cn/open-apis/authen/v1/access_token'
            user_resp = requests.post(
                user_url,
                json={'grant_type': 'authorization_code', 'code': code},
                headers={'Authorization': f'Bearer {access_token}'}
            )
            user_data = user_resp.json()

            if user_data.get('code') != 0:
                return Response({'message': '获取飞书用户信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            user_token = user_data.get('data', {}).get('access_token')
            
            # 获取用户详细信息
            detail_url = 'https://open.feishu.cn/open-apis/authen/v1/user_info'
            detail_resp = requests.get(
                detail_url,
                headers={'Authorization': f'Bearer {user_token}'}
            )
            detail_data = detail_resp.json()

            if detail_data.get('code') != 0:
                return Response({'message': '获取飞书用户详细信息失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            user_info = detail_data.get('data', {})
            open_id = user_info.get('open_id')
            union_id = user_info.get('union_id')
            avatar = user_info.get('avatar_big')

            feishu_user_data = {
                'open_id': open_id,
                'union_id': union_id,
                'name': user_info.get('name'),
                'avatar': user_info.get('avatar_big'),
                'email': user_info.get('enterprise_email'),
                'mobile': user_info.get('mobile'),
                'tenant_key': user_info.get('tenant_key')
            }

            # 查找或创建本地用户
            feishu_user_instance = FeiShuUser.objects.update_or_create(open_id=open_id, defaults=feishu_user_data)

            user = feishu_user_instance[0].user
            if not user:
                user_data = {
                    'username': open_id,
                    'first_name': user_info.get('name', ''),
                    'avatar': avatar,
                    'is_active': True
                }
                user = User.objects.update_or_create(username=open_id, defaults=user_data)[0]
                feishu_user_instance[0].user = user
                feishu_user_instance[0].save()
            else:
                user.avatar = avatar
                user.first_name = user_info.get('name', '')
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
