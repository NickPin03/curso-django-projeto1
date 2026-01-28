from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to="recipes/covers/%Y/%m/%d/", blank=True, default=""
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(
        self,
    ):  ## Pega o objeto/instancia referenciada/criado no momento e transforma em texto
        return self.title

    def get_absolute_url(self):
        return reverse(
            "recipes:recipe",
            args=(
                self.id,
            ),  ## Pega self.id da instancia que chamou essa funcao. Nesse caso a instancia recipe da view recipe
        )  ## Metodo que substitui ficar escrevendo "{% url 'recipes:recipe' recipe.id %}", se mudar aqui muda todos. Alem de apresentar btn pra ver receita no site, em admin

    def save(
        self, *args, **kwargs
    ):  ## Sempre que for salvar algo no banco de dados verifique o slug, pois se estiver vazio precisara de um valor, no caso do proprio title
        if not self.slug:
            slug = f"{slugify(self.title)}"
            self.slug = slug

        return super().save(
            *args, **kwargs
        )  ## Super() chama o metodo save original da classe mae (models.Model), processo de salvamento no banco de dados
