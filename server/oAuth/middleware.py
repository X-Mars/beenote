from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        try:
            # 尝试获取认证用户
            auth_result = self.jwt_auth.authenticate(request)
            if auth_result:
                user, _ = auth_result
                # 更新最近活跃时间
                user.last_active_at = timezone.now()
                user.save(update_fields=['last_active_at'])
        except:
            pass

        response = self.get_response(request)
        return response 