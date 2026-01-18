from django.shortcuts import render
from .forms import RegisterForm


# Create your views here.
def register_view(request):
    form = RegisterForm()  ## Para passarmos dados form p template
    return render(
        request,
        "author/pages/register_view.html",
        {
            "form": form,  ## A Etiqueta ("form"): É o nome que o arquivo HTML vai usar para chamar esses dados.
        },
    )
