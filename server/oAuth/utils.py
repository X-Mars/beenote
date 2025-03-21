from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import WeComConfig, FeiShuConfig, DingTalkConfig, GitHubConfig, GoogleConfig

class LoginQRCodeView(APIView):
    """获取第三方登录二维码"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # 获取各个第三方登录配置
            wecom_config = WeComConfig.objects.filter(enabled=True).first()
            feishu_config = FeiShuConfig.objects.filter(enabled=True).first()
            dingtalk_config = DingTalkConfig.objects.filter(enabled=True).first()
            github_config = GitHubConfig.objects.filter(enabled=True).first()
            google_config = GoogleConfig.objects.filter(enabled=True).first()

            # 构建返回数据
            response_data = {
                'wecom_url': None,
                'feishu_url': None,
                'dingtalk_url': None,
                'github_url': None,
                'google_url': None
            }

            # 企业微信登录URL
            if wecom_config:
                response_data['wecom_url'] = (
                    'https://open.work.weixin.qq.com/wwopen/sso/qrConnect?'
                    f'appid={wecom_config.corp_id}&'
                    f'agentid={wecom_config.agent_id}&'
                    f'redirect_uri={wecom_config.redirect_uri}'
                )

            # 飞书登录URL
            if feishu_config:
                response_data['feishu_url'] = (
                    'https://open.feishu.cn/open-apis/authen/v1/index?'
                    f'app_id={feishu_config.app_id}&'
                    f'redirect_uri={feishu_config.redirect_uri}'
                )

            # 钉钉登录URL
            if dingtalk_config:
                response_data['dingtalk_url'] = (
                    'https://login.dingtalk.com/oauth2/auth?'
                    f'client_id={dingtalk_config.client_id}&'
                    'response_type=code&'
                    'scope=openid&'
                    f'redirect_uri={dingtalk_config.redirect_uri}'
                )

            # GitHub登录URL
            if github_config:
                response_data['github_url'] = (
                    'https://github.com/login/oauth/authorize?'
                    f'client_id={github_config.client_id}&'
                    f'redirect_uri={github_config.redirect_uri}'
                )

            # Google登录URL
            if google_config:
                response_data['google_url'] = (
                    'https://accounts.google.com/o/oauth2/v2/auth?'
                    f'client_id={google_config.client_id}&'
                    'response_type=code&'
                    f'redirect_uri={google_config.redirect_uri}&'
                    'scope=openid email profile&'
                    'access_type=offline'
                )

            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=500) 