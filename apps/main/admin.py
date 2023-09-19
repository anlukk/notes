from django.contrib import admin
from .models import *

admin.site.register(Task)


@admin.register(Profiles)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'date_of_birth']


class SimpleNoteAdmin(admin.ModelAdmin):
    list_display = [
        'file_note',
        'time_create',
        'time_update',
        'name', 
        'text', 
        'slug',
    ]

    list_display_links = ('name', 'slug')
    list_editable = ()
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(SimpleNote, SimpleNoteAdmin)
admin.site.register(Category, CategoryAdmin)


