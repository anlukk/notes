from main.models import * 
from .serializers import SimpleNoteSerializer
from rest_framework.viewsets import GenericViewSet
from .permissions import IsOwnerOrReadOnly
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()
    
class NoteViewSet(ListModelMixin,  GenericViewSet):

    queryset = SimpleNote.objects.all()
    serializer_class = SimpleNoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
  



    

    