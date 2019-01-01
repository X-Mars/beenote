"""beenote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from oauth import views as oauth_views
from bee import views as bee_views
from oauth.master import obtain_jwt_token as new_obtain_jwt_token
from oauth.master import refresh_jwt_token as new_refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view



schema_view = get_swagger_view(title='beenote api')

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

router.register('userinfo', oauth_views.UserInfoViewSet)
router.register('note', bee_views.NoteViewsets)
router.register('notebook', bee_views.NoteBookViewsets)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-v1/login/', new_obtain_jwt_token),
    path('api-v1/token-refresh/', new_refresh_jwt_token),
    path('api-v1/logout/', oauth_views.LogoutViewSet.as_view({'get':'logout'})),
    path('api-v1/', include(router.urls)),
]
