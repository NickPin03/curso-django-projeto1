from django.contrib import admin

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin): ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "created_at",
        "is_published",
        "author",
    ]  ## Campos que quero que apareca no admin do django
    list_display_links = (
        "title",
        "created_at",
    )  ## Links para campos do admin django
    search_fields = (
        "id",
        "title",
        "description",
        "slug",
        "preparation_steps",
    )  # Barra pesquisa campos django admin
    list_filter = (
        "category",
        "author",
        "is_published",
        "preparation_steps_is_html",
    )
    list_per_page = 10  ## Vemos so 10 receitas por pag no admin do django
    list_editable = ("is_published",)  ## Habilita edicao no django Admin
    ordering = ("-id",)
    prepopulated_fields = {
        "slug": ("title",)
    }  ## Cria um slug ja baseado no titulo da recipe


admin.site.register(Category, CategoryAdmin)
