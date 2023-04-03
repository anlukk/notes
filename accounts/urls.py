from django.conf.urls import include
from django.urls import path
from .views import UserProfileView, register_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='registration_form'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    #path('users/<str:username>/', UserProfileView.as_view(), name='editprofile'),  
    path('user/settings/', UserProfileView.as_view(), name='editprofile'), 

]