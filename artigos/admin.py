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
    list_display = ('nome', 'artigo', 'conteudo_truncated', 'data_criacao', 'aprovado')
    list_filter = ('aprovado', 'data_criacao')
    search_fields = ('nome', 'email', 'conteudo')
    list_editable = ('aprovado',)
    actions = ['aprovar_comentarios']
    
    def conteudo_truncated(self, obj):
        return obj.conteudo[:50] + '...' if len(obj.conteudo) > 50 else obj.conteudo
    conteudo_truncated.short_description = "Comentário"
    
    def aprovar_comentarios(self, request, queryset):
        queryset.update(aprovado=True)
    aprovar_comentarios.short_description = "Aprovar comentários selecionados"
    
    def save_model(self, request, obj, form, change):
        import re
        # Verificar URLs no conteúdo
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        if url_pattern.search(obj.conteudo):
            from django.contrib import messages
            messages.error(request, "O comentário não pode conter URLs.")
            return
        super().save_model(request, obj, form, change)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'nome', 'pontuacao', 'comentario_truncated', 'data_criacao')
    list_filter = ('pontuacao', 'data_criacao')
    search_fields = ('nome', 'email', 'comentario')
    readonly_fields = ('artigo', 'nome', 'email', 'pontuacao', 'comentario', 'data_criacao')
    
    def comentario_truncated(self, obj):
        return obj.comentario[:50] + '...' if obj.comentario and len(obj.comentario) > 50 else obj.comentario
    comentario_truncated.short_description = "Comentário"
    
    def save_model(self, request, obj, form, change):
        # Validar pontuação entre 1 e 5
        if obj.pontuacao < 1 or obj.pontuacao > 5:
            from django.contrib import messages
            messages.error(request, "A pontuação deve ser entre 1 e 5.")
            return
        super().save_model(request, obj, form, change)