from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipes.models import Recipe


class DashboardRecipe(View):
    ## CBV é separado por metodos GET e POST -> View que edita receita ela lê a receita existente (get) e edita a mesma (post)
    def get_recipe(self, id):  ## Coleta a receita, reutilizamos
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
        )

        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, "Sua receita foi salva com sucesso!")
            return redirect(reverse("authors:dashboard_recipe_edit", args=(id,)))

        return self.render_recipe(form)
