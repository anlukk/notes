from os import path
from urllib.request import urlopen
from django.urls import reverse_lazy
from main.models import Profiles, SimpleNote
from main.utils import DataMixin
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import LoginForm, UserEditForm, ProfileEditForm, UserRegistrForm 
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SimpleNoteForm
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.postgres.search import(SearchVector, 
                                           SearchQuery, SearchRank, SearchHeadline)

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile



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
def image_upload(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST["username"]
        image_path = request.POST["src"] 
        image = NamedTemporaryFile()
        image.write(urlopen(path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.jpg' 
        image.name = name
        if image is not None:
            obj = Profiles.objects.create(username=username, image=image)  
            obj.save()
            context["path"] = obj.image.url  
            context["username"] = obj.username
        else :
            return redirect('/')
        return redirect('any_url')
    return render(request, 'editprofile.html', context=context)  

class SearchResultsList(LoginRequiredMixin, DataMixin, ListView):
    model = SimpleNote
    context_object_name = "Search"
    template_name = "main/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        search_vector = SearchVector("name", "text")
        search_query = SearchQuery(query)
        search_headline = SearchHeadline("text", search_query)
        return SimpleNote.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).annotate(headline=search_headline).filter(search=search_query).order_by("-rank")


def index(request):
    return render(request, 'main/index.html', {'title' : 'Main page of site'})


def FAQs(request):
    return render(request, 'main/FAQs.html')


class SimpleNote_View(LoginRequiredMixin, DataMixin, CreateView):
    form_class = SimpleNoteForm
    template_name = 'main/simple_note.html'
    raise_exception = True
    success_url = 'start'
    login_url = reverse_lazy('login')
    context_object_name = 'Simple Note'

@login_required
def my_note(request):
    return render(request, 'main/mynote.html')




@login_required
def choice_type(request):
    return render(request, 'main/choice_type.html')






