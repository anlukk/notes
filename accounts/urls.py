from django.conf.urls import include
from django.urls import path
from accounts.views import (UserProfileView, 
                            RegistrationExtraView,
                            )

urlpatterns = [
    # path('register/', register_view, name='registration_form'),

    path('register/', RegistrationExtraView.as_view(), name='registration_form'),

    path('', include('registration.backends.default.urls')),
    
    # path("<int:user_id>/", UserProfileView.as_view(), name="profile_view"),
    path('user/settings/', UserProfileView.as_view(), name='editprofile'), 

]