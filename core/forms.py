from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class UsuarioCadastroForm(UserCreationForm):
    tipo = forms.ChoiceField(choices=Perfil.TIPO_USUARIO, label="Tipo de Usuário")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'tipo']