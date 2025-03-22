#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/1/2 11:47
# @Author   : X-Mars
# @Site     : https://github.com/X-Mars
# @File     : oAuth/utils/__init__.py
# @Software : Pycharm

from .wecom import WeComLoginView
from .feishu import FeiShuLoginView
from .dingtalk import DingTalkLoginView
from .qrcode import LoginQRCodeView
from .github import GitHubLoginView
from .google import GoogleLoginView
from .gitlab import GitLabLoginView
from .gitee import GiteeLoginView

__all__ = [
    'WeComLoginView', 
    'FeiShuLoginView', 
    'DingTalkLoginView',
    'LoginQRCodeView',
    'GitHubLoginView',
    'GoogleLoginView',
    'GitLabLoginView',
    'GiteeLoginView'
]
