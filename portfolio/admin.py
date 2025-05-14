from django.contrib import admin
from .models import Disciplina, Projeto, Tecnologia, ImagemProjeto, Extras

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'semestre', 'docente')

@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'disciplina')
    filter_horizontal = ('tecnologias',)

@admin.register(ImagemProjeto)
class ImagemProjetoAdmin(admin.ModelAdmin):
    list_display = ('projeto',)

@admin.register(Extras)
class ExtrasAdmin(admin.ModelAdmin):
    list_display = ('projeto',)
