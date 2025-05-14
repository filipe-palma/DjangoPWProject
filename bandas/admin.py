from django.contrib import admin
from .models import Banda, Album, Musica

class AlbumInline(admin.TabularInline):
    model = Album
    extra = 1

class MusicaInline(admin.TabularInline):
    model = Musica
    extra = 1

@admin.register(Banda)
class BandaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano_formacao', 'genero', 'pais_origem')
    list_filter = ('genero', 'pais_origem')
    search_fields = ('nome', 'descricao')
    inlines = [AlbumInline]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'banda', 'ano_lancamento', 'gravadora')
    list_filter = ('ano_lancamento', 'banda')
    search_fields = ('titulo', 'descricao', 'banda__nome')
    inlines = [MusicaInline]

@admin.register(Musica)
class MusicaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'album', 'duracao', 'ordem')
    list_filter = ('album', 'album__banda')
    search_fields = ('titulo', 'letra', 'album__titulo', 'album__banda__nome')