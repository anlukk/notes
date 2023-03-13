from main.models import * 
from django.contrib.auth.models import User
from .serializers import SimpleNoteSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly


class NoteViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SimpleNoteSerializer


class SimpleNoteAPIList(generics.ListCreateAPIView):
    queryset = SimpleNote.objects.all()
    serializer_class = SimpleNoteSerializer
    permission_classes = (IsOwnerOrReadOnly)
    


    

    