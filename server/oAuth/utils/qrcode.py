#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/1/2 11:47
# @Author   : X-Mars
# @Site     : https://github.com/X-Mars
# @File     : oAuth/utils/qrcode.py
# @Software : Pycharm
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import WeComConfig, FeiShuConfig, DingTalkConfig, GitHubConfig
from urllib.parse import quote
import time
import hmac
import base64
import hashlib
import urllib.parse
from django.conf import settings

class LoginQRCodeView(APIView):
    """获取第三方登录二维码"""
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        try:
            # 获取各平台配置
            wecom_config = WeComConfig.objects.filter(enabled=True).first()
            feishu_config = FeiShuConfig.objects.filter(enabled=True).first()
            dingtalk_config = DingTalkConfig.objects.filter(enabled=True).first()
            github_config = GitHubConfig.objects.filter(enabled=True).first()

            result = {
                'wecom_url': None,
                'feishu_url': None,
                'dingtalk_url': None,
                'github_url': None
            }

            # 生成企业微信登录二维码URL
            if wecom_config:
                wecom_url = (
                    'https://login.work.weixin.qq.com/wwlogin/sso/login?'
                    f'login_type=CorpApp'
                    f'&appid={wecom_config.corp_id}'
                    f'&agentid={wecom_config.agent_id}'
                    f'&redirect_uri={wecom_config.redirect_uri}'
                    '&state=wecom'
                )
                result['wecom_url'] = wecom_url

            # 生成飞书登录二维码URL
            if feishu_config:
                feishu_url = (
                    'https://open.feishu.cn/open-apis/authen/v1/index'
                    f'?app_id={feishu_config.app_id}'
                    f'&redirect_uri={feishu_config.redirect_uri}'
                    '&state=feishu'
                )
                result['feishu_url'] = feishu_url

            # 生成钉钉登录二维码URL
            if dingtalk_config:
                timestamp = str(int(round(time.time() * 1000)))
                signature = self.get_dingtalk_signature(timestamp, dingtalk_config.client_secret)
                
                dingtalk_url = (
                    'https://login.dingtalk.com/oauth2/auth'
                    f'?client_id={dingtalk_config.client_id}'
                    f'&response_type=code'
                    f'&scope=openid'
                    f'&state=dingtalk'
                    f'&prompt=consent'
                    f'&redirect_uri={dingtalk_config.redirect_uri}'
                )
                result['dingtalk_url'] = dingtalk_url

            # 生成GitHub登录URL
            if github_config:
                github_url = (
                    'https://github.com/login/oauth/authorize'
                    f'?client_id={github_config.client_id}'
                    f'&redirect_uri={github_config.redirect_uri}'
                    '&scope=read:user,user:email'
                    '&state=github'
                )
                result['github_url'] = github_url

            return Response(result)

        except Exception as e:
            return Response({
                'message': '获取登录二维码失败',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_dingtalk_signature(self, timestamp: str, app_secret: str) -> str:
        """生成钉钉签名"""
        message = f"{timestamp}\n{app_secret}"
        hmac_code = hmac.new(
            app_secret.encode('utf-8'),
            message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return urllib.parse.quote_plus(base64.b64encode(hmac_code)) 