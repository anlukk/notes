from os import path
from urllib.request import urlopen
from django_tables2 import SingleTableMixin
from main.models import Profiles, SimpleNote, Category
from main.tables import MyNote_Table
from main.utils import DataMixin, archive_unnecessary_records
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .forms import( CategoryForm, SimpleNoteForm)
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.apps import apps
from django.contrib.auth import get_user_model


PER_PAGE = getattr(settings, "PAGINATOR_PER_PAGE", None)
User = get_user_model()


@login_required
def control_panel(request):
    return render(request,'main/control_panel.html', {'section': 'main page'})

@require_http_methods(["GET"])
def index(request):
    return render(request, 'main/index.html', {'title' : 'Main page of site'})


def faqs(request):
    return render(request, 'main/FAQs.html')


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


@login_required
@require_http_methods(["GET"])
def search(request):

    query = request.GET.get('q')
    results = SimpleNote.objects.filter(name__icontains=query) | SimpleNote.objects.filter(text__icontains=query)
    return render(request, 'main/search_results.html', {'results': results, 'query': query})


@login_required
def note_list(request):

    posts = SimpleNote.objects.all().order_by('-time_update')
    return render(request, 'main/note_list.html', {'posts': posts})


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
def choose_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # remove
            cat_id = form.cleaned_data['category']
            cat = Category.objects.get(id=cat_id)
            return redirect(cat.page_url)
    else:
        form = CategoryForm()

    return render(request, 'main/choose_category.html', {'form': form, 'cats': Category.objects.all()})
            

@login_required
def create_simple_note(request):

    if request.method == 'POST':
        form = SimpleNoteForm(request.POST, request.FILES)
        if form.is_valid():
            simple_note = form.save(commit=False)
            simple_note.user = request.user
            simple_note.save()
            from django.contrib import messages
            messages.success(request, 'Note created successfully!')
            return redirect('note_list', model_slug=simple_note.slug)
    else:
        form = SimpleNoteForm()
    return render(request, 'main/simple_note.html', {'form': form})


@method_decorator(login_required, name="dispatch")
class MyNoteTable_View(LoginRequiredMixin, DataMixin, SingleTableMixin, ListView): 
    notes = SimpleNote.objects.all().order_by('-time_update')
    table_class = MyNote_Table
    queryset = SimpleNote.objects.all()
    template_name = 'main/mynote_table.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        notes = SimpleNote.objects.all()  # Your list of posts here
        context['notes'] = notes
        return context
    
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
    






