from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth.models import NewUser, Roles
from oauth.serializer import UserInfoSerializer
from oauth.master import decode_token
import uuid

# Create your views here.

class LogoutViewSet(viewsets.ViewSet):

    def logout(self, request):
        request.user.jwt_secret = uuid.uuid4()
        request.user.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    serializer_class = UserInfoSerializer
    # permission_classes = (IsOwnerOrIsAdminUser, IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        username = request.user.username
        print(username)
        token = request.GET.get('token', None)
        user_info = decode_token(token=token)
        print(user_info)

        if(user_info['username'] == username):
            # user_info['username'] = username
            roles = Roles.objects.filter(newuser=request.user).values_list('roles', flat=True)
            print(roles)
            user_info['name'] = request.user.name
            user_info['roles'] = roles
            user_info['avatar'] = '../../../assets/images/logo.png'
            return Response(user_info)
        else:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)