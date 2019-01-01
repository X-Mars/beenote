#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018-12-29 09:43
# @Author  : MarsLiu
# @Site    : https://github.com/X-Mars
# @File    : master.py
# @Software: PyCharm

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import Serializer
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib import auth
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import jwt, time, uuid


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()

class NewVerificationBaseSerializer(Serializer):
    """
    Abstract serializer used for verifying and refreshing JWTs.
    """
    token = serializers.CharField()

    def validate(self, attrs):
        msg = 'Please define a validate method.'
        raise NotImplementedError(msg)

    def _check_payload(self, token):
        # Check payload valid (based off of JSONWebTokenAuthentication,
        # may want to refactor)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            payload = jwt.decode(token, verify = False)
            orig_iat = payload.get('orig_iat')
            if orig_iat:
                # Verify expiration
                refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA
                if isinstance(refresh_limit, timedelta):
                    refresh_limit = (refresh_limit.days * 24 * 3600 +
                                     refresh_limit.seconds)
                expiration_timestamp = orig_iat + int(refresh_limit)
                now_timestamp = time.time()

                if now_timestamp < expiration_timestamp:
                    return payload
                else:
                    msg = _('Refresh has expired.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('orig_iat field is required.')
                raise serializers.ValidationError(msg)

        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)

        return payload

    def _check_user(self, payload):
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)

        # Make sure user exists
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)

        return user

class NewRefreshJSONWebTokenSerializer(NewVerificationBaseSerializer):

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')

        if orig_iat:
            # Verify expiration
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)

            expiration_timestamp = orig_iat + int(refresh_limit)

            now_timestamp = time.time()

            if now_timestamp > expiration_timestamp:
                msg = _('Refresh has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat

        user.jwt_secret = uuid.uuid1()
        user.save()

        return {
            'token': jwt_encode_handler(new_payload),
            'id': user.id,
            'user': user
        }

class NewJSONWebTokenAPIView(JSONWebTokenAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            try:
                password = request.data['password']
                user.set_password(password)
                user.save()
            except KeyError:
                password = None

            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainJSONWebToken(NewJSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer

obtain_jwt_token = ObtainJSONWebToken.as_view()

class RefreshJSONWebToken(NewJSONWebTokenAPIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token
    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    serializer_class = NewRefreshJSONWebTokenSerializer

refresh_jwt_token = RefreshJSONWebToken.as_view()


def decode_token(token):
    user_info = jwt_decode_handler(token)
    # print(user_info)
    return user_info