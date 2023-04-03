
from django.shortcuts import render


def upload_note(request):
    if request.method == 'POST':
        from main.forms import FileUploadForm
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file_note = form.cleaned_data['file_note']
            
            with open(file_note.name, 'wb+') as destination:
                for chunk in file_note.chunks():
                    destination.write(chunk)
            
            return render(request, 'upload_success.html', {
                'name': name
                })
        
    else:
        form = FileUploadForm()
    return render(request)