from django.contrib import admin
from .models import *

admin.site.register(Task)


@admin.register(Profiles)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']


class SimpleNoteAdmin(admin.ModelAdmin):
    list_display = [
        'file_note',
        'time_create',
        'time_update',
        'is_printing',
        'name', 
        'text', 
        'slug',
    ]

    list_display_links = ('name', 'slug')

    list_editable = ()

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']



admin.site.register(SimpleNote, SimpleNoteAdmin)
admin.site.register(Category, CategoryAdmin)


