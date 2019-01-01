from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from bee.models import Note, NoteBook
from bee.serializer import NoteSerializer, NoteBookSerializer, NoteBookSerializerBase, NoteSerializerCreate
from rest_framework.response import Response

# Create your views here.

class NoteViewsets(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-id')
    serializer_class = NoteSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        self.serializer_class = NoteSerializerCreate
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class NoteBookViewsets(viewsets.ModelViewSet):
    queryset = NoteBook.objects.all()
    serializer_class = NoteBookSerializer

    def list(self, request, *args, **kwargs):
        type = request.query_params.get('type', None)
        print(type)
        if type == 'base':
            self.serializer_class = NoteBookSerializerBase
        self.queryset = NoteBook.objects.filter(user=request.user)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
