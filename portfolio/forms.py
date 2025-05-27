from django import forms
from .models import Projeto, Tecnologia, AreaInteresse, Disciplina, ImagemProjeto, Extras

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'video_demo': forms.URLInput(attrs={'class': 'form-control'}),
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
            'tecnologias': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'conceito': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'desafios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'repositorio': forms.URLInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AreaInteresseForm(forms.ModelForm):
    class Meta:
        model = AreaInteresse
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'projetos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tecnologias': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'disciplinas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'semestre': forms.TextInput(attrs={'class': 'form-control'}),
            'docente': forms.TextInput(attrs={'class': 'form-control'}),
            'moodle_url': forms.URLInput(attrs={'class': 'form-control'}),
            'pagina_uc': forms.URLInput(attrs={'class': 'form-control'}),
        }

class ImagemProjetoForm(forms.ModelForm):
    class Meta:
        model = ImagemProjeto
        fields = ['projeto', 'imagem']
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
class ExtrasForm(forms.ModelForm):
    class Meta:
        model = Extras
        fields = '__all__'
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-control'}),
            'info_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
