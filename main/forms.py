from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from .models import(
    Profiles, SimpleNote,
)

User = get_user_model()


class SimpleNoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Category not selected'

    class Meta:

        model = SimpleNote
        fields = ('name', 'text', 'file_note', 'cat')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
            'text': forms.Textarea(attrs={'cols':100, 'rows': 40}),
            'file_note': forms.ClearableFileInput(attrs={'multiple': True})
        }

