from django.contrib import admin
from django.db.models import Avg
from .models import Autor, Categoria, Tag, Artigo, Comentario, Avaliacao

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'website')
    search_fields = ('nome', 'email', 'bio')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome', 'descricao')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)

class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    readonly_fields = ('nome', 'email', 'website', 'conteudo', 'data_criacao')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0
    readonly_fields = ('nome', 'email', 'pontuacao', 'comentario', 'data_criacao')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'status', 'data_publicacao', 'media_avaliacoes', 'num_comentarios')
    list_filter = ('status', 'categorias', 'autor', 'data_publicacao')
    search_fields = ('titulo', 'subtitulo', 'conteudo')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_publicacao'
    filter_horizontal = ('categorias', 'tags')
    inlines = [ComentarioInline, AvaliacaoInline]
    
    def media_avaliacoes(self, obj):
        avg = obj.avaliacoes.aggregate(Avg('pontuacao'))['pontuacao__avg']
        return round(avg, 1) if avg else 0
    media_avaliacoes.short_description = 'Avaliação Média'
    
    def num_comentarios(self, obj):
        return obj.comentarios.count()
    num_comentarios.short_description = 'Comentários'

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'artigo', 'data_criacao', 'aprovado')
    list_filter = ('aprovado', 'data_criacao')
    search_fields = ('nome', 'email', 'conteudo')
    list_editable = ('aprovado',)
    actions = ['aprovar_comentarios']
    
    def aprovar_comentarios(self, request, queryset):
        queryset.update(aprovado=True)
    aprovar_comentarios.short_description = "Aprovar comentários selecionados"

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'nome', 'pontuacao', 'data_criacao')
    list_filter = ('pontuacao', 'data_criacao')
    search_fields = ('nome', 'email', 'comentario')
    readonly_fields = ('artigo', 'nome', 'email', 'pontuacao', 'comentario', 'data_criacao')