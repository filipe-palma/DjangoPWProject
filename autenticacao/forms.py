from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.',
        label='Nome de usuário',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Obrigatório. Informe um endereço de email válido.',
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Obrigatório. Informe seu nome.',
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        help_text='Obrigatório. Informe seu sobrenome.',
        label='Apelido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        help_text='Sua senha não pode ser muito semelhante às suas outras informações pessoais.<br>'
                 'Sua senha deve conter pelo menos 8 caracteres.<br>'
                 'Sua senha não pode ser uma senha comumente utilizada.<br>'
                 'Sua senha não pode ser inteiramente numérica.'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmação de senha',
        help_text='Digite a mesma senha que antes, para verificação.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9@./+\-_]+$', username):
            raise ValidationError('O nome de usuário só pode conter letras, dígitos e @/./+/-/_.')
        if len(username) > 150:
            raise ValidationError('O nome de usuário deve ter no máximo 150 caracteres.')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('A senha deve conter pelo menos 8 caracteres.')
        if password.isdigit():
            raise ValidationError('A senha não pode ser inteiramente numérica.')
        
        # Verificar semelhança com outras informações pessoais
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        
        personal_info = [username, email, first_name, last_name]
        for info in personal_info:
            if info and info.lower() in password.lower():
                raise ValidationError('A senha não pode ser muito semelhante às suas outras informações pessoais.')
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                "As senhas não coincidem."
            )
        
        return cleaned_data
