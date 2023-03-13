from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import *

router_v1 = DefaultRouter()
router_v1.register('Note', NoteViewSet)
# router_v1.register('Simple Note', SimpleNoteAPIList)

urlpatterns = [
     path("v1/", include(router_v1.urls))
]