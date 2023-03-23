from os import path
from urllib.request import urlopen
from django_tables2 import SingleTableMixin
from main.models import Profiles, SimpleNote
from main.tables import MyNote_Table
from main.utils import DataMixin, archive_unnecessary_records
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.utils.decorators import method_decorator

from .forms import( SimpleNoteForm)

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.apps import apps
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def control_panel(request):
    return render(request,'main/control_panel.html', {'section': 'main page'})


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
    return render(request, 'main/editprofile.html', context=context)  


def index(request):
    return render(request, 'main/index.html', {'title' : 'Main page of site'})


def faqs(request):
    return render(request, 'main/FAQs.html')


@login_required
def search(request):
    query = request.GET.get('q')
    results = SimpleNote.objects.filter(name__icontains=query) | SimpleNote.objects.filter(text__icontains=query)
    return render(request, 'main/search_results.html', {'results': results, 'query': query})


# class MyNote_List_View(LoginRequiredMixin, TemplateView):
#     template_name = 'main/post_list.html'
#     raise_exception = True
#     success_url = 'start'
#     login_url = reverse_lazy('login')
#     context_object_name = 'My Note'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         notes = SimpleNote.objects.all()  # Your list of posts here
#         context['notes'] = notes
#         return context
    

@login_required
def note_list(request):
    posts = SimpleNote.objects.all().order_by('-time_update')
    return render(request, 'main/mynote.html', {'posts': posts})


@login_required
def edit_note(request, pk):
    note = get_object_or_404(SimpleNote, pk=pk)
    if request.method == "POST":
        form = SimpleNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = SimpleNoteForm(instance=note)
    return render(request, 'main/edit_note.html', {'form': form, 'note': note})


@login_required
def archive_view(request, model_slug):

    try:
        model = apps.get_model(app_label='main', model_name=model_slug)
    except LookupError:
        raise Http404("Model does not exist")
    
    note = get_object_or_404(SimpleNote, pk=model_slug)

    context = {
        'note': note,
        'name': note.name,
        'text': note.text,
        'cat_selected': note.cat_id,
    }
    
    queryset = archive_unnecessary_records(model)
    return render(request, 'main/archive.html', {'records': queryset}, context=context)

@login_required
def choice_type(request):
    #
    return render(request, 'main/choice_type.html')


@method_decorator(login_required, name="dispatch")
class Create_SimpleNote_View(LoginRequiredMixin, DataMixin, CreateView):
    form_class = SimpleNoteForm
    template_name = 'main/simple_note.html'
    context_object_name = 'Simple Note'


@method_decorator(login_required, name="dispatch")
class MyNoteTable_View(LoginRequiredMixin, DataMixin, SingleTableMixin, ListView): 
    notes = SimpleNote.objects.all().order_by('-time_update')
    table_class = MyNote_Table
    queryset = SimpleNote.objects.all()
    template_name = 'main/mynote_table.html'
    context_object_name = 'My Note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = SimpleNote.objects.all()  # Your list of posts here
        context['notes'] = notes
        return context
    







