from django.shortcuts import render
from main.forms import FileUploadForm


def upload_note(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file_note = form.cleaned_data['file_note']
            with open(file_note.name, 'wb+') as destination:
                for chunk in file_note.chunks():
                    destination.write(chunk)
            
            return render(request, 'upload_success.html', {'name': name})
        
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
 

