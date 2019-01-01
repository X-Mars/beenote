from django.contrib import admin
from bee.models import Note, NoteBook

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'notebook', 'type', 'create_time', 'update_time', 'user')
    list_display_links = ('id', 'title', 'notebook', 'type', 'create_time', 'update_time', 'user')


class NoteBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'create_time')
    list_display_links = ('id', 'name', 'user', 'create_time')

admin.site.register(Note, NoteAdmin)
admin.site.register(NoteBook, NoteBookAdmin)