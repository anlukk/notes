from main.models import SimpleNote
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from main.forms import SimpleNoteForm
from django.contrib.auth.decorators import login_required
from unidecode import unidecode
from slugify import slugify


@login_required
@require_http_methods(["GET", "POST"])
def create_simple_note(request):
    owner = SimpleNote.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SimpleNoteForm(request.POST, request.FILES)
        if form.is_valid():
            simple_note = form.save(commit=False)
            simple_note.user_id = request.user.id

            loting = unidecode(simple_note.name)

            simple_note.slug = slugify(loting)

            if not SimpleNote.objects.filter(
                slug=simple_note.slug).exists():
                simple_note.save()
                form.save()
                return redirect('note_list')
            else:
                form.add_error('slug', 'This slug already exists.')
    else:
        form = SimpleNoteForm()
    return render(
        request, 'main/simple_note.html', {'form': form, 'owner': owner})
