from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):  ## É um formulário não atrelado a um model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Type your username")
        add_placeholder(self.fields["password"], "Type your password")

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
