from main.models import SimpleNote
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from main.models import SimpleNote
from main.utils import archive_unnecessary_records
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from main.services.search import *
from main.services.note import *
from main.services.categories import *


@login_required
def archive_view(request, model_slug):
    try:
        model = apps.get_model(
            app_label='main', 
            model_name=model_slug
            )
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
    return render(request, 'main/archive.html', {
        'records': queryset,
        }, context=context)
