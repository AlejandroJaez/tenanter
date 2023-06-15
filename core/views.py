from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def test_view(request: HttpRequest) -> HttpResponse:
    """
    Main (or index) view.

    Returns rendered default page to the user.
    Typed with the help of ``django-stubs`` project.
    """
    print("test view")
    return render(request, "core/index.html")