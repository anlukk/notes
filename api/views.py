from main.models import * 
from django.contrib.auth.models import User
from .serializers import SimpleNoteSerializer
from rest_framework.viewsets import GenericViewSet
from .permissions import IsOwnerOrReadOnly
from rest_framework.mixins import ListModelMixin



class NoteViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SimpleNoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return self.request.user.accounts.all()



    

    