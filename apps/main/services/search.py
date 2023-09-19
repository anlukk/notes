from main.models import SimpleNote
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
@require_http_methods(["GET", "POST"])
def search_view(request):

    query = request.GET.get('q')
    results = None
    if query:
        results = SimpleNote.objects.filter(
            Q(name__icontains=query) |
            Q(text__icontains=query)
        )
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'main/search_results.html', context)