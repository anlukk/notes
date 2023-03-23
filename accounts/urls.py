from django.conf.urls import include
from django.urls import path
from .views import register_view, edit_profile_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('editprofile', edit_profile_view, name='editprofile'),  

]