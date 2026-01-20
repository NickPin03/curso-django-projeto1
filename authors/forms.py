from django import forms  ## Importamos classes para criar forms
from django.contrib.auth.models import User  ## Puxamos de um model que já existe
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):  ## Cria valores pro atributo attr
    existing_attr = field.widget.attrs.get(attr_name, "")  # pega o valor de attr
    field.widget.attrs[attr_name] = (
        f"{existing_attr} {attr_new_val}".strip()
    )  ## acrescenta novo valor em attr


def add_placeholder(  ## Apenas para acrescentar placeholder
    field, placeholder_val
):  ## Função para adicionar especificamente placeholder
    add_attr(field, "placeholder", placeholder_val)


## Para criar forms do Django, baseamos em classes
class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(
            self.fields["username"], "Your username"
        )  ## Cria attrs por classe. Tirei o parametro placeholder e passei por função
        add_placeholder(self.fields["email"], "Your e-mail")
        add_placeholder(self.fields["last_name"], "Ex: Doe")
        add_attr(self.fields["username"], "css", "a-css-class")

    """     self.fields["username"].widget.attrs[
            "placeholder"
        ] = "Que legal"  """  ## Forma de aplicar valor ao placeholder sem sobescrever.

    """    Como funciona o  self.fields["username"].widget.attrs["placeholder"] = "Que legal" 

        1. (self) self.fields -> é um dicionário que o django cria ( Chave são valores que criou em fields)
        2. (widget) Atributo do objeto, controla o HTML
        3. (attrs) Dentro de widget tem um dicionário chamado attrs (atributos)
        4. (placeholder) Você a chave do dicionário attrs, placeholder, e define o valor dela.

Se pudessemos visualizar ficaria assim a estrutura:
 { 
    "fields": {
        "first_name": { ... },
        "username": {  # <--- Você entrou aqui
            "label": "Username",
            "help_text": "",
            "widget": { # <--- Entrou aqui
                "template_name": "django/forms/widgets/text.html",
                "attrs": { # <--- Entrou aqui
                    "class": "vTextField",
                    "placeholder": "Que legal" # <--- ALTEROU ISSO!
                }
            }
        },
        "email": { ... }
    }
}   
    """

    password = forms.CharField(  ## Sempre que for sobescrever um campo existente em meta já passe tudo
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Your password"}),
        error_messages={"required": "Password must not be empty"},
        help_text=(
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be"
            "at least 8 characters"
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat your password"}),
    )

    class Meta:  ## Classe que guarda meta-dados (configurações do form)
        model = User  ## Atrelado ao model User
        fields = [  ## Ele cria uma tag <input name="first_name"> para cada input e seu atributo pra name
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]  ## Campos que quero ver no formulário

        labels = {  ## Consigo renomear os labels (descrições dos inputs)
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "E-mail",
            "password": "Password",
        }

        help_texts = {  ## Textos de ajuda que aparecem abaixo do campo
            "email": "The e-mail must be valid.",
        }

        error_messages = {  ## Mensagens customizadas para erros de validação
            "username": {
                "required": "This field must not be empty",
            }
        }

        widgets = {  ## Para colocar classes CSS e atributos HTML, precisamos sobrescrever os widgets
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Type your first name here",
                    "class": "input text-input",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Type your password here"
                }  ## sobescrever fora da class meta
            ),
        }

    def clean_password(self):
        data = self.cleaned_data.get("password")

        if "atenção" in data:
            raise ValidationError(
                "Não digite %(pipoca)s no campo password",
                code="invalid",
                params={"pipoca": '"atenção"'},
            )

        return data

    def clean_first_name(
        self,
    ):  ## Limpa os dados para um campo específico --> Quando a regra depende apenas daquele campo. Ex: "O nome não pode ser John Doe" ou "O usuário deve ter mais de 18 anos".
        data = self.cleaned_data.get(
            "first_name"
        )  ## Pega dados campo first_name, cleaned data é um dicionário com os dados que já passaram pela validação do django

        if "John Doe" in data:  ## Se houver o valor 'John Doe' em data mostrará o erro
            raise ValidationError(
                "Não digite %(value)s no campo first name",
                code="invalid",
                params={"value": '"John Doe"'},
            )

        return data

    def clean(
        self,
    ):  ## Utilizado depois de todos os métodos clean individuais serem utilizados.
        cleaned_data = (
            super().clean()
        )  ## Pegamos o metodo clean da super classe para verificar os dados
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            password_confirmation_error = ValidationError(
                "Password and password2 must be equal", code="invalid"
            )  ## Se for mesmo erro vrio uma variável para não repetir
            raise ValidationError(  ## Dicionário de erros
                {
                    "password": password_confirmation_error,
                    "password2": [
                        password_confirmation_error,
                        ## Another error, -> Posso colocar mais erros se quiser
                    ],
                }
            )

    """ O que entendi de como esta classe lê os seus campos:
    Quando eu pego o objeto, não pego só o field e um input por vez ,
    mas um por de vez de toda a classe. Então ele percorre cada item do dicionario por vez,
    tipo estou no input de first_name, ele pega só os dicionários de first name, { field.label}
    ele pega o dicionario label do first name e se os outros dicionarios tiverem algo pra first name
    ou html chamar ele mostra. Em seguida, vai para o próximo campo (input)
     """
