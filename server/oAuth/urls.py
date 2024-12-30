from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, UserInfoView, UserViewSet, GroupViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    # 包含路由器生成的URL
    path('', include(router.urls)),
    
    # 其他URL保持不变
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserInfoView.as_view(), name='user_info'),
    path('stats/', views.get_stats, name='user-stats'),
] 