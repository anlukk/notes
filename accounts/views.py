from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from registration.backends.default.views import RegistrationView


from .forms import RegistrationExtraForm
from solien_web.settings import PAGINATOR_PER_PAGE

from .forms import LoginForm

from django.contrib.auth import login as auth_login, authenticate

PER_PAGE = getattr(settings, "PAGINATOR_PER_PAGE", None)
User = get_user_model()


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


# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'rgeistration/registration_form.html', {'form': form})

class RegistrationExtraView(RegistrationView):

    form_class = RegistrationExtraForm
    template_name = 'registration/registration_form.html'

@method_decorator(login_required, name="dispatch")
class UserProfileView(View):

    def get(self, request):

        # user = get_object_or_404(User)
        user = User.objects.get(username=request.user.username)
        context = {
            'user': user,
            # 'username': username,
            }
        return render(request, 'main/editprofile.html', context=context)


