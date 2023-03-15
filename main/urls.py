from . import views
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('editprofile', views.edit, name='editprofile'),  
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='start'),
    path('control_panel', views.control_panel, name='control_panel'),
    path('FAQs', views.FAQs, name='FAQs'),
    path('search', views.search, name='search'),
    path('simple_note', views.simple_note, name='simple_note')
]
