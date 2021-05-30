from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms

from .models import *

class clienteForma(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['user']

class PedidoForma(ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class CrearUsuarioForma(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
