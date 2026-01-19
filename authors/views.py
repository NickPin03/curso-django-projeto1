from django.http import Http404
from django.shortcuts import render, redirect

from .forms import RegisterForm


# Create your views here.
def register_view(request):
    ## request.session["number"] = request.session.get("number") or 1
    ## request.session["number"] += 1 - Soma valor com 1 e atribui resultado
    ## Criamos um dicionário na request para guardar dados, aqui nº vezes user acessou register. Cada vez: entra url register -> pega valo guardado number, soma + 1  e apresenta no template
    register_form_data = request.session.get(
        "register_form_data", None
    )  ## Busca dados armazenados do post
    form = RegisterForm(
        register_form_data
    )  ## Para passarmos dados form p template se houver,se não none

    return render(
        request,
        "author/pages/register_view.html",
        {
            "form": form,  ## A Etiqueta ("form"): É o nome que o arquivo HTML vai usar para chamar esses dados.
        },
    )


def register_create(request):  ## IMP: Essa view só vai ler os dados do POST.
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session["register_form_data"] = POST  ## Estou guardando os dados de POST.

    form = RegisterForm(POST)

    return redirect(
        "authors:register"
    )  ## Dados são enviados para register por get, elimina problema de recarregar página e reenviar form por post


## Problema: Não tenho como retornar dados para outra página. Essa view é para criar user e retornar erro, mas quero voltar pra register com os dados. Para isso usamos sessões, guardo no navegador do usuário

"""     return render( -> Não vamos mostrar dados no template, mas retorna eles validados para view create
        request,
        "author/pages/register_view.html",
        {
            "form": form,
        },
    ) """
