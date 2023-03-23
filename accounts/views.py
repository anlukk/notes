from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from main.models import Profiles

from .forms import LoginForm, ProfileEditForm, UserEditForm

from django.contrib.auth import login as auth_login, authenticate

PER_PAGE = getattr(settings, "PAGINATOR_PER_PAGE", None)
User = get_user_model()


@login_required
def edit_profile_view(request):
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


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# class ProfileView(View):

#     def get_queryset(self, request, author):

#         tags = request.GET.getlist("filters")
#         if not tags:
#             recipes = Profiles.objects.filter(author=author).exclude(
#                 tags__slug__in=tags)
#         else:
#             recipes = Profiles.objects.filter(author=author).filter(
#                 tags__slug__in=tags)
#         return recipes

#     # def get(self, request, user_id):

#     #     author = get_object_or_404(User, id=user_id)
#     #     recipes = self.get_queryset(request, author)
#     #     paginator = Paginator(recipes.filter(author=author), PER_PAGE)
#     #     page_number = request.GET.get("page")
#     #     page = paginator.get_page(page_number)
#     #     tags = Tag.objects.all()
#     #     context = {"author": author,
#     #                "page": page,
#     #                "paginator": paginator,
#     #                "tags": tags,
#     #                }
#     #     return render(request, "recipes/profile.html", context)