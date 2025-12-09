from django.shortcuts import render
# Create your views here.


def home(request):  # servidor recebe request # Ao invés de httresponse, usamos render, mas lembre que django não sabe que recipes existe
    return render(request, 'recipes/home.html', context={'name': 'Luiz Otávio', })
