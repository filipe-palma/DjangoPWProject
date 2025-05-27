from django import forms
from .models import Projeto, Tecnologia, AreaInteresse

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'

class AreaInteresseForm(forms.ModelForm):
    class Meta:
        model = AreaInteresse
        fields = '__all__'
