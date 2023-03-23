from . import views
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from main.views import (
    Create_SimpleNote_View, MyNoteTable_View, 
    archive_view, edit_note
    )


urlpatterns = [
    path('', views.index, name='start'),
    
    path('control_panel', views.control_panel, name='control_panel'),

    path('FAQs', views.faqs, name='FAQs'),

    path('simple_note', Create_SimpleNote_View.as_view(), name='simple_note'),

    path('archive/<int:model_slug>/', archive_view, name='archive'),

    path('mynote/edit_note', edit_note, name='edit_note'),

    path('mynote_table', MyNoteTable_View.as_view(), name='mynote_table' ),

    path('mynote', views.note_list, name='mynote' ),

    path('mynote/search/', views.search, name='search_results'),


]
