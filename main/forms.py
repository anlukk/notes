from django.contrib.auth.models import User
from django import forms
from .models import(
    Profiles, SimpleNote,
)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrForm(forms.ModelForm):
   password = forms.CharField(label='password', widget=forms.PasswordInput)
   password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

   class Meta:
       model = User 
       fields = ('username', 'first_name', 'email')

   def clean_password2(self):
       cd = self.cleaned_data
       if cd['password'] != cd['password2']:
           raise forms.ValidationError('Passwords don\'t match')
       return cd['password2']


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    
    class Meta:
        model = Profiles
        fields = ("date_of_birth",) 


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

