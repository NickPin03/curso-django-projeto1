import re
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


def strong_password(password):
    regex = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$"
    )  ## Valida se password tem alguma letra de a-z, A-Z e 0-9 e 8 caracteres se houver qualquer um desses, é validado

    if not regex.match(password):
        raise ValidationError(
            (
                "Password must have at least one uppercase letter, "
                "one lowercase letter and one number. The length should be "
                "at least 8 characters."
            ),
            code="invalid",
        )
