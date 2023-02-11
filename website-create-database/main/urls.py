from . import views
from django.urls import path
from . import views 
#from . views import LoginUser
from django.contrib.auth import views as auth_views


urlpatterns = [
   #path('login', views.user_login, name='login'),
   #path('login', views.LoginUser.as_view(), name='login'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='start'),
   #path('DOC', views.about, name='finally'),
    path('sol', views.sol, name='sol'),
    path('FAQs', views.FAQs, name='FAQs'),
    path('search', views.search, name='search'),
    path('features', views.features, name='features'),
    path('editprofile', views.edit, name='editprofile')
]
