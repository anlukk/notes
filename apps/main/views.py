from django.views import View
from django_tables2 import SingleTableMixin
from main.models import SimpleNote
from main.tables import MyNote_Table
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from main.services.files import image_upload, text_file_upload
from main.services.search import search_view
from main.services.note import edit_note, create_simple_note
from main.services.categories import choose_category
from main.services.archive import archive_view
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import SimpleNoteForm


PER_PAGE = getattr(settings, "PAGINATOR_PER_PAGE", None)
User = get_user_model()


@login_required
def control_panel(request):
    return render(request,'main/control_panel.html', {'section': 'main page'})

@require_http_methods(["GET"])
def index(request):
    return render(request, 'main/index.html', {'title' : 'Main page of site'})

@login_required
@require_http_methods(["POST"])
def search(request):
    return search_view(request)

@login_required
@require_http_methods(["POST"])
def upload_image(request):
    return image_upload(request)

@login_required
@require_http_methods(["POST"])
def create_note(request):
    return create_simple_note(request)


@login_required
@require_http_methods(["GET"])
def categories(request):
    return choose_category(request)

@login_required
@require_http_methods(["GET", "POST"])
def archive(request):
    return archive_view(request)

@login_required
@require_http_methods(["GET", "POST"])
def text_file_upload_view(request, filename):
    return text_file_upload(request, filename)

def faqs(request):
    faqs = [
        {'question': 'How to create a new note?', 'answer': 'Go to the note creation page and fill out the form.'},
        {'question': 'How to delete a note?', 'answer': 'Go to the page with detailed information about the note and click the "Delete" button.'},
        {'question': 'Can I edit notes?', 'answer': 'Yes, on the page with detailed information about the note there is an "Edit" button.'},
    ]
    contact_list = SimpleNote.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'faqs': faqs,
        'title': 'FAQs',
        'contact_list': contact_list
    }

    return render(request, 'main/FAQs.html', context)


@method_decorator(login_required, name="dispatch")
class MyNoteTable_View(LoginRequiredMixin, SingleTableMixin, ListView): 
    table_class = MyNote_Table
    queryset = SimpleNote.objects.all()
    template_name = 'main/mynote_table.html'


@method_decorator(login_required, name="dispatch")
class NoteListView(View):

    def get(self, request):
        notes = SimpleNote.objects.filter(user=request.user)
        paginator = Paginator(notes, 10)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'notes': notes,
            'page_obj': page_obj
        }
        return render(request, 'main/note_list.html', context=context)  
    
    def post(self, request):
        note_id = request.POST.get('note_id')
        if note_id:
            note = get_object_or_404(SimpleNote, id=note_id)
            note.delete()
            return redirect("note_list")
        else:
            print("Note ID not provided in POST request")
        return redirect("note_list") 
    

@method_decorator(login_required, name="dispatch")
class NoteView(View):
    slug_url_kwarg = 'simple_note_slug'
    context_object_name = 'simple_note'

    def get(self, request, simple_note_slug):
        owner = SimpleNote.objects.filter(user=request.user)
        note = get_object_or_404(
            SimpleNote, 
            slug=simple_note_slug,
            )
        
        return render(request, 'main/view_note.html', {
            'owner': owner, 'simple_note': note})
    
    def post(self, request, pk):
        note = get_object_or_404(SimpleNote, pk=pk)
        if request.method == "POST":
            form = SimpleNoteForm(request.POST, instance=note)
            if form.is_valid():
                note = form.save(commit=False)
                note.save()
                return redirect('note_detail', pk=note.pk)
        else:
            form = SimpleNoteForm(instance=note)

        return redirect("view_note") 
    
    def get_context_data(self, *, object_list=None, **kwargs): 
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=context['simple_note'])
        
        return dict(list(context.items()) + list(c_def.items()))