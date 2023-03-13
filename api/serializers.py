from rest_framework import serializers
from main.models import SimpleNote, Category


class SimpleNoteSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta: 
        model = SimpleNote
        field = "__all__"



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = "__all__"
