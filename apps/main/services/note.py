from main.models import SimpleNote
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from main.forms import SimpleNoteForm
from django.contrib.auth.decorators import login_required


@login_required
@require_http_methods(["GET", "POST"])
def create_simple_note(request):
    owner = SimpleNote.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SimpleNoteForm(request.POST, request.FILES)
        if form.is_valid():
            simple_note = form.save(commit=False)
            simple_note.user_id = request.user.id
            if not SimpleNote.objects.filter(slug=simple_note.slug).exists():
                simple_note.save()
                form.save()
                return redirect('note_list')
            else:
                form.add_error('slug', 'This slug already exists.')
    else:
        form = SimpleNoteForm()
    return render(request, 'main/simple_note.html', {'form': form, 'owner': owner})


@login_required
@require_http_methods(["GET", "POST"])
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

    return render(request, 'main/edit_note.html', {
        'note': note, 'form': form})
