from urllib.request import urlopen
from main.models import Profiles
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.views.decorators.http import require_http_methods
import os
from django.http import HttpResponse
from django.conf import settings


@require_http_methods(["GET", "POST"])
@login_required
def image_upload(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST["username"]
        try:
            path = request.POST["path"]
            response = urlopen(path)
            if response.getcode() == 200:
                image = NamedTemporaryFile(delete=False)
                image.write(response.read())
                image.flush()
                image = File(image)
                name = str(image.name).split('\\')[-1]

                name += '.jpg'
                image.name = name

                obj = Profiles.objects.create(
                    username=username, image=image)
                obj.save()
                context["path"] = obj.image.url
                context["username"] = obj.username
            else:
                return redirect('/')
        except Exception as e:
            return redirect('/'), e

        return redirect('any_url')
    return render(request, 'main/editprofile.html', context=context)



@login_required
def text_file_upload(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'note.txt')
    if not os.path.exists(file_path):
        return HttpResponse(
            f"File {filename} not found", status=404)
    with open(file_path, 'r') as f:
        file_data = f.read()

    response = HttpResponse(file_data, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="note.txt"'

    return response
