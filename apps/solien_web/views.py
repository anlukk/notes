from django.shortcuts import render


def permission_denied(request, exception):
    return render(
        request, "403.html",
        {
            "path": request.path,
            "title": "Error 403",
        },
        status=403
    )

def page_not_found(request, exception):
    return render(
        request, "404.html",
        {
            "path": request.path,
            "title": "Error 404",
        },
        status=404
    )


def server_error(request):
    return render(
        request, "500.html",
        {
            "path": request.path,
            "title": "Error 500",
        },
        status=500
    )
