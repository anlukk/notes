from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import (UserProfileView, 
                            RegistrationExtraView,
                            )

urlpatterns = [
    # path('register/', register_view, name='registration_form'),

    path('register/', RegistrationExtraView.as_view(), name='registration_form'),
    path('', include('registration.backends.default.urls')),
    # path("<int:user_id>/", UserProfileView.as_view(), name="profile_view"),
    path('user/settings/', UserProfileView.as_view(), name='editprofile'), 


    # path('login', auth_views.LoginView.as_view(), name='login'),
    # path('logout', auth_views.LogoutView.as_view(), name='logout'),

]