from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get("preparation_steps"), "class", "span-2")
        add_attr(
            self.fields.get("cover"), "class", "span-2"
        )  ## Pega campos e coloca classe span-2 neles para ocuparem 2 colunas

    class Meta:
        model = Recipe
        fields = (
            "title",
            "description",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
        )
