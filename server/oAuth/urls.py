from django.urls import path
from .views import LoginView, UserInfoView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserInfoView.as_view(), name='user_info'),
    path('stats/', views.get_stats, name='user-stats'),
] 