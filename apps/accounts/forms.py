from django.contrib.auth import get_user_model
from django import forms
from registration.forms import RegistrationForm

User = get_user_model()

class RegistrationExtraForm(RegistrationForm):
    
    class Meta(RegistrationForm.Meta):
        fields = RegistrationForm.Meta.fields + ('first_name',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# class UserRegistrForm(forms.ModelForm):
#    password = forms.CharField(label='password', widget=forms.PasswordInput)
#    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

#    class Meta:
#        model = User 
#        fields = ('username', 'first_name', 'email')

#    def clean_password2(self):
#        cd = self.cleaned_data
#        if cd['password'] != cd['password2']:
#            raise forms.ValidationError('Passwords don\'t match')
#        return cd['password2']
