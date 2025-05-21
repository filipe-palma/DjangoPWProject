from django import forms
from .models import Artigo, Comentario, Avaliacao

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'subtitulo', 'conteudo', 'imagem_capa', 'status', 'categorias', 'tags', 'destaque', 'fonte_original']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do artigo'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtítulo ou breve descrição'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Conteúdo do artigo...'}),
            'imagem_capa': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'categorias': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'destaque': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fonte_original': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL da fonte original (se aplicável)'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'website', 'conteudo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail (não será publicado)'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Seu website (opcional)'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Seu comentário...'}),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nome', 'email', 'pontuacao', 'comentario']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail (não será publicado)'}),
            'pontuacao': forms.Select(attrs={'class': 'form-select'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Seu comentário sobre este artigo...'}),
        }
