from django.urls import path
from .views import (
    ArtigoDetailView, ArtigoListView, ArtigoCreateView, ArtigoUpdateView, 
    ArtigoDeleteView, ComentariosListView, approve_comment, delete_comment
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
    path('comentarios/<int:comment_id>/excluir/', delete_comment, name='comentario-delete'),
]
