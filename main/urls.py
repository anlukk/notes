from . import views
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from main.views import Create_SimpleNote_View, MyNote_View, edit_note


urlpatterns = [
    path('editprofile', views.edit, name='editprofile'),  
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='start'),
    path('control_panel', views.control_panel, name='control_panel'),
    path('FAQs', views.FAQs, name='FAQs'),
    path('simple_note', Create_SimpleNote_View.as_view(), name='simple_note'),
    path('mynote/archive', views.archive, name='archive'),
    path('mynote/edit_note', edit_note, name='edit_note'),
     path('mynote', MyNote_View.as_view(), name='mynote' ),

]
