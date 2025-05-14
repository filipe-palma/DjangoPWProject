from django import forms
from .models import Artigo, Comentario, Avaliacao

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'subtitulo', 'conteudo', 'imagem_capa', 'status', 'categorias', 'tags', 'destaque', 'fonte_original']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 6}),
            'categorias': forms.CheckboxSelectMultiple(),
            'tags': forms.CheckboxSelectMultiple(),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'website', 'conteudo']

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nome', 'email', 'pontuacao', 'comentario']
        widgets = {
            'pontuacao': forms.Select(),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }
