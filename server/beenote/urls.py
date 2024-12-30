from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from note.views import NoteViewSet, GroupViewSet, NoteStatsView
from oAuth.views import UserViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('oAuth.urls')),
    path('api/', include(router.urls)),
    path('api/notes/stats/', NoteStatsView.as_view(), name='note-stats'),
] 