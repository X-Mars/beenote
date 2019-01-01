#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018-12-29 20:48
# @Author  : MarsLiu
# @Site    : https://github.com/X-Mars
# @File    : serializer.py.py
# @Software: PyCharm

from rest_framework import serializers
from bee.models import Note, NoteBook
from oauth.models import NewUser


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'type', 'create_time', 'update_time')

class NoteSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'type', 'create_time', 'update_time', 'notebook', 'user')

class NoteBookSerializerBase(serializers.ModelSerializer):

    class Meta:
        model = NoteBook
        fields = ('id', 'name', 'create_time', 'user')


class NoteBookSerializer(serializers.ModelSerializer):
    note = NoteSerializer(many=True)
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = {
            'name': obj.name,
            'path': 'notebook/' + str(obj.id),
            'component': "() => import('@/views/documentation/notebook/notebook')",
            'meta': {
                'title': obj.name,
                'icon': 'folder',
                'roles': ['admin', 'users']
            }
        }
        return children

    class Meta:
        model = NoteBook
        fields = ('id', 'name', 'user', 'note', 'create_time', 'children')

