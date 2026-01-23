from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

from .forms import LoginForm, RegisterForm


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
        "authors/pages/register_view.html",
        {
            "form": form,  ## A Etiqueta ("form"): É o nome que o arquivo HTML vai usar para chamar esses dados.
            "form_action": reverse(
                "authors:register_create"
            ),  ## Dados para informar onde quero que form envie dados. Com template form, não podemos especificar lá, pois será reutilizável
        },
    )


def register_create(request):  ## IMP: Essa view só vai ler os dados do POST.
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session["register_form_data"] = POST  ## Estou guardando os dados de POST.

    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)  ## criptografa a senha
        user.save()
        messages.success(request, "Your user is created, please log in.")

        del request.session[
            "register_form_data"
        ]  ## Limpa dados, já que salvei no banco de dados
        return redirect(
            reverse("authors:login")
        )  ## Após criar usuário já mando ele pra página de login

    """  data = form.save(commit=False)  - Não salva formulário mas guarda seus dados
        data.outro_campo = "outro_valor" - Adiciona valores ao formulário depois que tudo foi validado """

    return redirect(
        "authors:register"
    )  ## Dados são enviados para register por get, elimina problema de recarregar página e reenviar form por post


def login_view(request):
    form = LoginForm()  ## Pegamos dados form login
    return render(
        request,
        "authors/pages/login.html",  ## Redireciona p/ template login
        {
            "form": form,
            "form_action": reverse("authors:login_create"),
        },  ## Manda dados form, template form pega esses dados. No caso crio primeiro o formulário com classe, passo pro template e pra onde esse form vai ser enviado depois de clicar no btn enviar dele
    )


def login_create(request):
    if not request.POST:  ## Erro caso não seja POST
        raise Http404()

    form = LoginForm(request.POST)  ## Pego os dados enviados do form de login
    login_url = reverse("authors:login")

    if (
        form.is_valid()
    ):  ## Caso formulário seja válido. Ou seja, tenha seus campos preenchidos e válidos
        authenticated_user = authenticate(
            username=form.cleaned_data.get(
                "username", ""
            ),  ## Pega valor de username/password, se não válido, retorna vazio. Vai até o banco de dados e verifica se existe username e password correspondentes
            password=form.cleaned_data.get("password", ""),
        )

        if (
            authenticated_user is not None
        ):  ## 1. Se não enviaram form vazio e é válido com dados do servidor
            messages.success(
                request, "You are logged in."
            )  ## 2. Se username e password estiverem corretos
            login(
                request, authenticated_user
            )  ## 3. Se tudo correto usuário irá logar. OBS: Precisamos request pra atrelar usuário a requisição, com cookies. Criando sessão para ele
        else:
            messages.error(
                request, "Invalid credentials"
            )  ## 4. Dados válidos, mas username ou password incorretos
    else:
        messages.error(
            request, "Invalid username or password"
        )  ## Se formulário não for válido, vazio, etc.
    return redirect(reverse("authors:dashboard"))


@login_required(
    login_url="authors:login", redirect_field_name="next"
)  ## Só pode acessar essa página se logado. Caso tente entrar numa página que precise estar logado, primeiro loga e depois o redirect direciona para onde queria ir antes. Next fala onde  queria ir.
def logout_view(request):
    if not request.POST:  ## Se pedido logout não for POST, retorna a pag login
        return redirect(reverse("authors:login"))

    if request.POST.get("username") != request.user.username:
        return redirect(reverse("authors:login"))

    logout(request)
    return redirect(
        reverse("authors:login")
    )  ## Problema: Alguém pode mandar esse link de logout, e se eu estiver logado irei deslogar (CSRF)


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False, author=request.user
    )  ## Receitas do dashboard do autor serão apenas as não publicadas e receitas apenas do autor da sessao
    return render(
        request,
        "authors/pages/dashboard.html",
        context={
            "recipes": recipes,
        },
    )


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()  ## Irei editar receitas do user. OBS: Filter retorna uma queryset, é uma lista de coisas, quando usamos instance no form, queremos uma recipe, por isso pegamos a primeira com filter. OBS: Poderiamos usar o get como mostra na aula 184.

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(request.POST or None, instance=recipe)
    ## Formulário que pode receber instância (bound form) ou pode ser um form novo. Ele tem uma instância de recipe, quando ele clicar em save, salvará nesta instancia.
    """ Resumo: 
           Instance = Serve para ligar o formulário a um objeto que já existe no banco de dados. No caso pegamos até o ID específico dele. É preenchido todos os campos do HTML
           None (GET) = Quando você  entrar na página de edição o POST está vazio, None.
           request.POST = Quando você clicar no btn "Enviar" do form, os dados saem do navegador e chegam na view. Django cria form com novos dados que digitou no navegador, mas salvará no banco apenas com save().
    """

    return render(
        request,
        "authors/pages/dashboard_recipe.html",
        context={
            "form": form,
        },
    )


## Problema: Não tenho como retornar dados para outra página. Essa view é para criar user e retornar erro, mas quero voltar pra register com os dados. Para isso usamos sessões, guardo no navegador do usuário

"""     return render( -> Não vamos mostrar dados no template, mas retorna eles validados para view create
        request,
        "author/pages/register_view.html",
        {
            "form": form,
        },
    ) """
