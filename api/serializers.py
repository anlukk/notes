from rest_framework import serializers
from main.models import SimpleNote, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleNoteSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta: 
        model = SimpleNote
        exclude = ('name', 'text', 'time_create')
        depth = 3
        field = "all"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        field = "all"
