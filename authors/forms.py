from django import forms  ## importamos classes p criar forms
from django.contrib.auth.models import User  ## Puxo de um model que ja existe

## Para criar forms do django, baseamos em classes


class RegisterForm(forms.ModelForm):
    class Meta:  ## Classe que guarda meta-dados
        model = User  ## Atrelado form User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]  ## Campos que quero ver -  fields = "__all__" -> se quero ver todos campos
        # exclude = ['first_name'] -> Mostra todos os campos menos first_name

    labels = {  ## Consigo renomear os labels
        "username": "Username",
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "E-mail",
        "password": "Password",
    }
