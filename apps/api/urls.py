from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import *

router_v1 = DefaultRouter()

router_v1.register(r'SimpleNote', SimpleNoteViewSet, basename='SimpleNote')
router_v1.register(r'Category', CategoryViewSet, basename='Category')


urlpatterns = [
     path("v1/", include(router_v1.urls)),
]