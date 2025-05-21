from django import forms
import re
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
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Seu comentário (apenas texto)...'}),
        }
    
    def clean_conteudo(self):
        conteudo = self.cleaned_data['conteudo']
        
        # Check if the content contains URLs
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        if url_pattern.search(conteudo):
            raise forms.ValidationError("O comentário não pode conter URLs.")
        
        return conteudo

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['pontuacao']
        widgets = {
            'pontuacao': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_pontuacao(self):
        pontuacao = self.cleaned_data['pontuacao']
        
        if pontuacao < 1 or pontuacao > 5:
            raise forms.ValidationError("A pontuação deve ser um valor entre 1 e 5.")
            
        return pontuacao
