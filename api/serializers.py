from rest_framework import serializers
from main.models import SimpleNote, Category

class SimpleNoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = SimpleNote
        field = (
            'name',
            'text',
            'file_note',
        )
