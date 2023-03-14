from .forms import UserRegistrForm 
from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, UserEditForm, ProfileEditForm
from . models import Task
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import SimpleNoteForm


""" 
Comment: this module uses the authorization form @login_forms (1 module)
For this version, the registration form is not taken into account

The form for adding an account contradicts the registration form. 
add form is not active due to the fact that it creates an already created account in an authorized
"""

@login_required
def control_panel(request):
    return render(request,'main/control_panel.html', {'section': 'main page'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrForm(request.POST)
        if user_form.is_valid():
            #create new users
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'main/login.html', {'new_user': new_user})
    else: 
        user_form = UserRegistrForm()
        return render(request, 'main/login.html', {'user_form': user_form})
    

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'main/editprofile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def search(request):
    return render(request, 'main/search.html')


def index(request):
    return render(request, 'main/index.html', {'title' : 'Main page of site'})


def FAQs(request):
    return render(request, 'main/FAQs.html')

def simple_note(request):
    return render(request, 'main/simple_note.html')


