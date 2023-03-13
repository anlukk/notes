from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import *

router_v1 = DefaultRouter()

router_v1.register('SimpleNote', NoteViewSet, basename='SimpleNote')


urlpatterns = [
     path("v1/", include(router_v1.urls)),
]