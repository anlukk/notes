from django.contrib.auth import get_user_model
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import SimpleNote
from .models import Category


User = get_user_model()


class SimpleNoteForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['cat'].empty_label = 'Category not selected'

    class Meta:
        model = SimpleNote
        fields = ['name', 'text', 'file_note']
        text = forms.CharField(widget = CKEditor5Widget())

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
            'file_note': forms.ClearableFileInput(attrs={'multiple': True})
        }

        

class CategoryForm(forms.Form):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.RadioSelect)

    class Meta:
        model = Category
        fields = ['name', 'slug']

    