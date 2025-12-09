from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.


def home(request):  # servidor recebe request # Ao invés de httresponse, usamos render, mas lembre que django não sabe que recipes existe
    return render(request, 'recipes/home.html', context={'name': 'Luiz Otávio', })


def contato(request):  # servidor recebe request
    return render(request, 'temp.html')


def sobre(request):  # servidor recebe request
    return HttpResponse('Sobre')
