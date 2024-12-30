from django.contrib import admin
from .models import Note, NoteGroup

@admin.register(NoteGroup)
class NoteGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creator', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'creator', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('group', 'created_at', 'updated_at')
