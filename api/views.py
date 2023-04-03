from main.models import * 
from .serializers import SimpleNoteSerializer, CategorySerializer
from rest_framework.viewsets import GenericViewSet 
from .permissions import IsOwnerOrReadOnly
from rest_framework.mixins import ListModelMixin
from django.contrib.auth import get_user_model
from rest_framework.response import Response


User = get_user_model()
    
    
class SimpleNoteViewSet(ListModelMixin,  GenericViewSet):

    queryset = SimpleNote.objects.all()
    serializer_class = SimpleNoteSerializer

    def perform_create(self, serializer):

        username = User.objects.get(id=self.request.data["id"])
        user = self.request.user
        serializer.save(username=username, user=user)
        return super().perform_create(serializer)

    def get_queryset(self):

        query = self.request.query_params.get("query")
        if query is None:
            return SimpleNote.objects.none()
        queryset = SimpleNote.objects.filter(name__startswith=query
                                             ).values("name")
        return queryset
    
    def list(self, request): 

        owner = SimpleNote.objects.filter(user=request.user)
        serializer = self.get_serializer(owner, many=True)
        return Response(serializer.data)

        
class CategoryViewSet(ListModelMixin, GenericViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        query = self.request.query_params.get("query")
        queryset = Category.objects.all()
        return queryset



    

    