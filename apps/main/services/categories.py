from main.models import Category
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main.forms import CategoryForm

@login_required
def choose_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat_id = form.cleaned_data['category']
            cat = Category.objects.get(id=cat_id)
            return redirect(cat.page_url)
    else:
        form = CategoryForm()

    return render(request, 'main/choose_category.html', {
        'form': form, 
        'cats': Category.objects.all()
        })