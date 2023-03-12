from django.contrib import admin
from .models import *

admin.site.register(Task)


@admin.register(Profiles)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']


class SimpleNoteAdmin(admin.ModelAdmin):
    list_display = (
        'file_path',
        'file_note',
        'time_create',
        'time_update',
        'is_printing',
        'name', 
        'text', 
        'slug',
        )

admin.site.register(SimpleNote, SimpleNoteAdmin)


