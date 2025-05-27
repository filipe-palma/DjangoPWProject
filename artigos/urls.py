from django.urls import path
from .views import (
    ArtigoDetailView, ArtigoListView, ArtigoCreateView, ArtigoUpdateView, 
    ArtigoDeleteView, ComentariosListView, approve_comment, delete_comment,
    # New AJAX views
    ajax_criar_categoria, ajax_editar_categoria, ajax_apagar_categoria,
    ajax_criar_tag, ajax_editar_tag, ajax_apagar_tag,
    # Author AJAX views
    ajax_criar_autor, ajax_editar_autor, ajax_apagar_autor
)

app_name = 'artigos'

urlpatterns = [
    path('', ArtigoListView.as_view(), name='artigo-list'),
    path('novo/', ArtigoCreateView.as_view(), name='artigo-create'),
    path('<slug:slug>/', ArtigoDetailView.as_view(), name='artigo-detail'),
    path('<slug:slug>/editar/', ArtigoUpdateView.as_view(), name='artigo-update'),
    path('<slug:slug>/apagar/', ArtigoDeleteView.as_view(), name='artigo-delete'),
    
    # URLs para moderação de comentários (apenas para gestores)
    path('comentarios/moderacao/', ComentariosListView.as_view(), name='comentarios-moderacao'),
    path('comentarios/<int:comment_id>/aprovar/', approve_comment, name='comentario-approve'),
    path('comentarios/<int:comment_id>/excluir/', delete_comment, name='comentario-delete'),    # AJAX URLs para categorias
    path('ajax/categorias/criar/', ajax_criar_categoria, name='ajax-criar-categoria'),
    path('ajax/categorias/editar/<int:id>/', ajax_editar_categoria, name='ajax-editar-categoria'),
    path('ajax/categorias/apagar/<int:id>/', ajax_apagar_categoria, name='ajax-apagar-categoria'),
    
    # AJAX URLs para tags
    path('ajax/tags/criar/', ajax_criar_tag, name='ajax-criar-tag'),
    path('ajax/tags/editar/<int:id>/', ajax_editar_tag, name='ajax-editar-tag'),
    path('ajax/tags/apagar/<int:id>/', ajax_apagar_tag, name='ajax-apagar-tag'),
    
    # AJAX URLs for authors
    path('ajax/autores/criar/', ajax_criar_autor, name='ajax-criar-autor'),
    path('ajax/autores/editar/<int:id>/', ajax_editar_autor, name='ajax-editar-autor'),
    path('ajax/autores/apagar/<int:id>/', ajax_apagar_autor, name='ajax-apagar-autor'),
]
