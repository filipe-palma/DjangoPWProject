from django import forms
from .models import Projeto, Tecnologia, AreaInteresse, Disciplina, ImagemProjeto, Extras

class FormWithBootstrapMixin:
    """
    Mixin para adicionar classes Bootstrap a todos os campos do formulário
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Adiciona classes a todos os campos para melhorar a acessibilidade
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control shadow-sm'
            
            # Adiciona rótulos como placeholders se não existirem
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label
                
            # Adiciona feedback de validação
            field.widget.attrs['data-bs-toggle'] = 'tooltip'
            
            # Melhoria de acessibilidade
            field.widget.attrs['aria-label'] = field.label if field.label else field_name

class ProjetoForm(FormWithBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Título do projeto',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Descrição detalhada do projeto'
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'URL do repositório no GitHub'
            }),
            'video_demo': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'URL da demonstração em vídeo'
            }),
            'disciplina': forms.Select(attrs={'class': 'form-select shadow-sm'}),
            'tecnologias': forms.SelectMultiple(attrs={
                'class': 'form-select shadow-sm select2-multiple',
                'size': '5',
                'data-placeholder': 'Selecione as tecnologias'
            }),
            'conceito': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 3,
                'placeholder': 'Conceito do projeto'
            }),
            'desafios': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 3,
                'placeholder': 'Principais desafios encontrados'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrupa campos por categorias para melhorar a organização visual
        self.fields['titulo'].widget.attrs.update({'autocomplete': 'off'})
        
        # Melhoria de legibilidade para campos de múltipla escolha
        if 'tecnologias' in self.fields:
            self.fields['tecnologias'].help_text = 'Selecione múltiplas tecnologias utilizando Ctrl+Click (ou Cmd+Click no Mac)'

class TecnologiaForm(FormWithBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Nome da tecnologia'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Descrição da tecnologia'
            }),
            'repositorio': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'URL do repositório/documentação oficial'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control shadow-sm',
                'accept': 'image/*'
            }),
        }

class AreaInteresseForm(FormWithBootstrapMixin, forms.ModelForm):
    class Meta:
        model = AreaInteresse
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Nome da área de interesse'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Descrição da área de interesse'
            }),
            'projetos': forms.SelectMultiple(attrs={
                'class': 'form-select shadow-sm',
                'size': '5'
            }),
            'tecnologias': forms.SelectMultiple(attrs={
                'class': 'form-select shadow-sm',
                'size': '5'
            }),
            'disciplinas': forms.SelectMultiple(attrs={
                'class': 'form-select shadow-sm',
                'size': '5'
            }),
        }
        
class DisciplinaForm(FormWithBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Nome da disciplina'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ano letivo',
                'min': '2000',
                'max': '2050'
            }),
            'semestre': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Semestre (ex: 1º, 2º)'
            }),
            'docente': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Nome do docente responsável'
            }),
            'moodle_url': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'URL da página no Moodle'
            }),
            'pagina_uc': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'URL da página oficial da UC'
            }),
        }

class ImagemProjetoForm(FormWithBootstrapMixin, forms.ModelForm):
    class Meta:
        model = ImagemProjeto
        fields = ['projeto', 'imagem']
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-select shadow-sm'}),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control shadow-sm',
                'accept': 'image/*'
            }),
        }
        
class ExtrasForm(FormWithBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Extras
        fields = '__all__'
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-select shadow-sm'}),
            'info_adicional': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Informações adicionais sobre o projeto'
            }),
        }
