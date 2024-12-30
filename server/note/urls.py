from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, NoteGroupViewSet

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='note')
router.register('groups', NoteGroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
] 