from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
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
        fields = ['name', 'text', 'file_note', 'cat']
        text = forms.CharField(widget = CKEditor5Widget())
        

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form_input'}),
        #     # 'text': forms.Textarea(attrs={'cols':100, 'rows': 40}),
        #     # "text": CKEditor5Widget(
        #     #       attrs={"class": "django_ckeditor_5"}, config_name="comment"
        #     #   ),
        #     'file_note': forms.ClearableFileInput(attrs={'multiple': True})
        # }

