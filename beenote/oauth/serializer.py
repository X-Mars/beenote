#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018-12-29 13:34
# @Author  : MarsLiu
# @Site    : https://github.com/X-Mars
# @File    : serializer.py
# @Software: PyCharm
from rest_framework import serializers
from oauth.models import NewUser
from django.contrib.auth.models import Group as UserGroup


class UserGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('id', 'name')

class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    groups = UserGroupSerializer(many=True, read_only=True)
    groups_id = serializers.ListField(write_only=True, required=True)

    class Meta:
        model = NewUser
        fields = ('id', 'username', 'email', 'groups', 'groups_id', 'name')
        write_only_fields = ('password',)