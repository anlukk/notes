from . import views
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from main.views import SearchResultsList, SimpleNote_View


urlpatterns = [
    path('editprofile', views.edit, name='editprofile'),  
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='start'),
    path('control_panel', views.control_panel, name='control_panel'),
    path('FAQs', views.FAQs, name='FAQs'),
    path('search', SearchResultsList.as_view(), name='search'),
    path('simple_note', SimpleNote_View.as_view(), name='simple_note')
]
