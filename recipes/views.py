import os

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.pagination import make_pagination
from django.views.generic import ListView

from recipes.models import Recipe

PER_PAGES = int(
    os.environ.get("PER_PAGE", 6)
)  ## pega valor da variável de ambiente, transforma em int pois vem string


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None  ## paginação do próprio cbv
    context_object_name = "recipes"  ## objeto com as recipes
    ordering = ["-id"]  ## ordenada por padrão por id decrescente
    template_name = "recipes/pages/home.html"  ## template da view

    def get_queryset(  ## Retorna lista objetos apenas receitas publicadas
        self, *args, **kwargs
    ):  ## pega informações da url, caso classe pai precisar
        qs = super().get_queryset(  ## Query set está na classe pai, então preciso usar o super pra utilizar engrenagem dele, o que está aqui é apenas da recipelistviewbase, a engrenagem especifica que só usa getqueryset
            *args, **kwargs
        )  ## Passei os dados para classe pai, é como se para utilizar este metodo eu precisasse inicializar ele, ele já sabe que meu model é recipe e puxa os dados do banco. Isso faz mesma coisa que filter quando utilizei funções na view.
        qs = qs.filter(
            is_published=True,
        )
        return qs  ## retorna lista com objetos publicados, guarda em self.object_list

    def get_context_data(
        self, *args, **kwargs
    ):  ## Para enviar os dados por contexto a outro template
        ctx = super().get_context_data(
            *args,
            **kwargs,  ## Metodo sabe que é uma instancia de recipes (self), então cria um dicionário pra ela.
        )  ## Construimos o dicionario de contexto
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get("recipes"), PER_PAGES
        )
        ctx.update({"recipes": page_obj, "pagination_range": pagination_range})
        return ctx


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by("-id")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(
        request,
        "recipes/pages/home.html",
        context={
            "recipes": page_obj,  ## retorna uma das várias páginas que foram divididas por make_pagination
            "pagination_range": pagination_range,  ## lista de números que devem aparecer
        },
    )


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by("-id")
    )

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGES
    )  ## Toda vez se repete o 9, não queremos isto, vamos supor que eu mude isso. Preciso usar constante

    return render(
        request,
        "recipes/pages/category.html",
        context={
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "title": f"{recipes[0].category.name} - Category | ",
        },
    )


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe,
        pk=id,
        is_published=True,
    )

    """ Representação conceitual da instância 'recipe' na memória
        recipe = {
        'id': 5,
        'title': 'Lasanha à Bolonhesa',
        'slug': 'lasanha-a-bolonhesa',
        'author_id': 1,
        'category_id': 3,
    
     }  """

    return render(
        request,
        "recipes/pages/recipe-view.html",
        context={
            "recipe": recipe,
            "is_detail_page": True,
        },
    )


def search(request):
    search_term = request.GET.get("q", "").strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by("-id")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(
        request,
        "recipes/pages/search.html",
        {
            "page_title": f'Search for "{search_term}" |',
            "search_term": search_term,
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "additional_url_query": f"&q={search_term}",
        },
    )
