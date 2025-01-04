from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, UserInfoView, UserViewSet, GroupViewSet,
    WeComConfigViewSet, FeiShuConfigViewSet, DingTalkConfigViewSet,
    GitHubConfigViewSet, health_check
)
from .utils import WeComLoginView, FeiShuLoginView, DingTalkLoginView, LoginQRCodeView, GitHubLoginView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'wecom-config', WeComConfigViewSet)
router.register(r'feishu-config', FeiShuConfigViewSet)
router.register(r'dingtalk-config', DingTalkConfigViewSet)
router.register(r'github-config', GitHubConfigViewSet)

urlpatterns = [
    # 包含路由器生成的URL
    path('', include(router.urls)),
    
    # 其他URL保持不变
    path('login/', LoginView.as_view(), name='login'),
    path('wecom/login/', WeComLoginView.as_view(), name='wecom_login'),
    path('feishu/login/', FeiShuLoginView.as_view(), name='feishu_login'),
    path('dingtalk/login/', DingTalkLoginView.as_view(), name='dingtalk_login'),
    path('github/login/', GitHubLoginView.as_view(), name='github_login'),
    path('login/qrcode/', LoginQRCodeView.as_view(), name='login_qrcode'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserInfoView.as_view(), name='user_info'),
    path('stats/', views.get_stats, name='user-stats'),
    path('health/', health_check, name='health_check'),
] 