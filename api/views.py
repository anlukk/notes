from main.models import * 
from .serializers import SimpleNoteSerializer, CategorySerializer
from rest_framework.viewsets import GenericViewSet 
from .permissions import IsOwnerOrReadOnly
from rest_framework.mixins import ListModelMixin
from django.contrib.auth import get_user_model


User = get_user_model()
    
class NoteViewSet(ListModelMixin,  GenericViewSet):

    queryset = SimpleNote.objects.all()
    serializer_class = SimpleNoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]



    

    