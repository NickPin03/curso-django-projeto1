from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import (
    method_decorator,
)  ## Usamos para decorar metodos de classe
from django.contrib.auth.decorators import login_required
from django.views import View
from recipes.models import Recipe


## dispatch decide se chama met get ou post
@method_decorator(
    login_required(login_url="authors:login", redirect_field_name="next"),
    name="dispatch",
)
class DashboardRecipe(View):
    def __init__(
        self,
        *args,
        **kwargs,  ## Args é uma lista de argumentos sem nome e kwargs, um dicionário de argumentos com nome (Ex: id=121)
    ):
        """Init é executado ao receber uma requisição, ao criar uma instância na memoria.
        Se você não usar init aqui, ele usará da classe view.
        print("Este é o meu INIT")"""

        self.atributo_meu = "Que massa"  ## Como self foi criado no momento do "nascimento" do objeto todos os outros metodos da classe podem ver ele
        super().__init__(
            *args,
            **kwargs,  ## Args e kwargs entregam para classe pai view, os dados da caixa recebidos na criação do objeto
        )  ## Preciso chamar init da classe pai para funcionar

    ## CBV: é separado por metodos GET e POST -> View que edita receita ela lê a receita existente (get) e edita a mesma (post)
    def get_recipe(self, id=None):  ## Coleta a receita, reutilizamos
        print(self.atributo_meu)
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

        if not recipe:
            raise Http404()

        return recipe

    def render_recipe(self, form):  ## Função para renderizar template receita
        return render(
            self.request, "authors/pages/dashboard_recipe.html", context={"form": form}
        )

    def get(  ## Função para quando entrar na página sem enviar dados novos
        self, request, id
    ):
        """Self é um objeto da classe DashBoardRecipe, acessa as propriedades da view/classe; Self aqui é como um espaço na memória. Objeto que django criou para processar nesse momento
        IMP: Com self já recebemos tudo, a request, etc, não precisando de vários parametros de funçao
        """
        """    recipe = Recipe.objects.filter( -- get_recipe(self, id) -> Elimina este trecho de código
            is_published=False,
            author=request.user,
            pk=id,
        ).first()

        if not recipe:
            raise Http404() """

        recipe = self.get_recipe(
            id
        )  ## Retorna receita através do objeto da página (self) atrelado ao metodo da classe, passando o id que recebemos por get no link

        form = AuthorRecipeForm(
            instance=recipe
        )  ## Instancia para vincular form a recipe selecionada
        return self.render_recipe(form)

        """    form = AuthorRecipeForm( -- Metodo get não usamos POST, só instância
            data=request.POST or None, files=request.FILES or None, instance=recipe
        ) 
        """

        """     if form.is_valid(): -- Não precisa validar form pois aqui só puxa dados get
            # Agora, o form é válido e eu posso tentar salvar
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, "Sua receita foi salva com sucesso!")
            return redirect(reverse("authors:dashboard_recipe_edit", args=(id,)))

        return render(
            request, "authors/pages/dashboard_recipe.html", context={"form": form}
        )
        """

    def post(self, request, id):  ## Função para receber dados post do form
        """Self é um objeto da classe DashBoardRecipe, acessa as propriedades da view/classe; Self aqui é como um espaço na memória. Objeto que django criou para processar nesse momento
        Self = O objeto da página que criamos que guarda
        IMP: Com self já recebemos tudo, a request, etc, não precisando de vários parametros de funçao
        """
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=request.POST or None, files=request.FILES or None, instance=recipe
        )  ## O request.POST é uma bagunça de textos: "title=Bolo&prep_time=60". O form organiza isso em gavetas limpas: form.cleaned_data['title'].

        """ Explicação dados form:
        Navegador: Você digitou no campo <input name="title">.

        No request.POST: O dado chegou como um texto bruto: {'title': 'Bolacha de nat'}.

        No form: O formulário validou e limpou o texto.

        No recipe: Ao fazer form.save(commit=False), o Django pegou o valor do formulário e "carimbou" dentro da propriedade .title do objeto recipe.
        """

        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar
            recipe = form.save(commit=False)
            """ breakpoint() """
            """ print(f"TIPO DO OBJETO: {type(recipe)}")  # Vai mostrar que é uma Recipe
            print(
                f"DADOS TIPO DICIONÁRIO: {recipe.__dict__}"
            )  # Mostra todos os valores internos """

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, "Sua receita foi salva com sucesso!")
            return redirect(reverse("authors:dashboard_recipe_edit", args=(id,)))

        return self.render_recipe(form)


@method_decorator(
    login_required(login_url="authors:login", redirect_field_name="next"),
    name="dispatch",
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *arg, **kwargs):
        recipe = self.get_recipe(
            self.request.POST.get("id")
        )  ## O id é recebido pelo form, não via get mais, dentro dos atributos de POST
        recipe.delete()
        messages.success(self.request, "Deleted succesfully.")
        return redirect(reverse("authors:dashboard"))


""" De onde vem o id?
O id não vem exatamente da "implementação da URL", mas sim da ativação da URL pelo navegador.

A URL é acessada: O navegador pede algo como /authors/dashboard/recipe/121/delete/.

O Django lê o ID: Ele extrai o número 121 da rota definida no seu urls.py.

O Objeto nasce: O Django instancia DashboardRecipeDelete, criando o self na memória.

O Setup armazena: O Django executa o setup() (aquele que você viu antes) e guarda o 121 dentro de self.kwargs['id'].

A Entrega: O Django chama o seu método post(self, request, id) e passa o valor 121 para o argumento id da função. """
