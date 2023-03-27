from os import path
from urllib.request import urlopen
from django.views import View
from django_tables2 import SingleTableMixin
from main.models import Profiles, SimpleNote, Category
from main.tables import MyNote_Table
from main.utils import DataMixin, archive_unnecessary_records
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .forms import CategoryForm, SimpleNoteForm
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib import messages


PER_PAGE = getattr(settings, "PAGINATOR_PER_PAGE", None)
User = get_user_model()


@login_required
def control_panel(request):
    return render(request,'main/control_panel.html', {'section': 'main page'})


@require_http_methods(["GET"])
def index(request):
    return render(request, 'main/index.html', {'title' : 'Main page of site'})


@login_required
def note_list(request):

    owner = SimpleNote.objects.filter(user=request.user)
    return render(request, 'main/note_list.html', {'owner': owner})


def faqs(request):

    contact_list = SimpleNote.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/FAQs.html', {'page_obj': page_obj, 'title': 'FAQs'})


@login_required
@require_http_methods(["GET", "POST"])
def search(request):

    query = request.GET.get('q')
    results = SimpleNote.objects.filter(
        name__icontains=query
        ) | SimpleNote.objects.filter(
        text__icontains=query
        )
    return render(request, 'main/search_results.html', {'results': results, 'query': query})


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
@require_http_methods(["GET", "POST"])
def create_simple_note(request):

    owner = SimpleNote.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SimpleNoteForm(request.POST, request.FILES)
        if form.is_valid():
            simple_note = form.save(commit=False)
            simple_note.user_id = request.user.id
            simple_note.save()
            form.save()
            return redirect('note_list')
    else:
        form = SimpleNoteForm()
    # context = {
    #     'simple_note': simple_note,
    #     'name': simple_note.name,
    #     'cat_selected': simple_note.cat_id
    # }
    return render(
        request, 
        'main/simple_note.html', 
        {'form': form, 'owner': owner}
        )


@method_decorator(login_required, name="dispatch")
class MyNoteTable_View(LoginRequiredMixin, DataMixin, SingleTableMixin, ListView): 
    notes = SimpleNote.objects.all().order_by('-time_update')
    table_class = MyNote_Table
    queryset = SimpleNote.objects.all()
    template_name = 'main/mynote_table.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        notes = SimpleNote.objects.all()  
        context['notes'] = notes
        return context
    

@method_decorator(login_required, name="dispatch")
class NoteView(View):

    def get(self, request, simple_note_slug):

        owner = SimpleNote.objects.filter(user=request.user)
        note = get_object_or_404(SimpleNote, slug=simple_note_slug)
        context = {
            'note': note,
            'name': note.name,
            'cat_selected': note.cat_id,
        }
        return render(request, 'main/view_note.html', context=context)


@method_decorator(login_required, name="dispatch")
class NoteCategory(View):
    model = SimpleNote
    allow_empty = False

    def get(self, request):
        
        return render(request, 'main/note_list.html')
    
    def get_queryset(self):
        return SimpleNote.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            name='Category - ' + str(context['notes'][0].cat),
            cat_selected=context['notes'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))








