from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from core.models import Product


# Create your views here.
def test_view(request: HttpRequest) -> HttpResponse:
    """
    Main (or index) view.

    Returns rendered default page to the user.
    Typed with the help of ``django-stubs`` project.
    """
    print("test view")
    return render(request, "core/index.html")


class ProductCreateView(CreateView):
    model = Product
    fields = ["name"]
    success_url = reverse_lazy("create")


class ProductListView(ListView):
    model = Product
    fields = ["name"]


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
