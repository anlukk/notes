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

    def get(self, serializer):

        username = User.objects.get(id=self.request.data["id"])
        user = self.request.user
        serializer.save(username=username, user=user)
        return super().perform_create(serializer)

        
class CategoryViewSet(ListModelMixin, GenericViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        query = self.request.query_params.get("query")
        queryset = Category.objects.all()
        return queryset



    

    