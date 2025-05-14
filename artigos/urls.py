from django.urls import path
from .views import ArtigoDetailView, ArtigoListView, ArtigoCreateView, ArtigoUpdateView, ArtigoDeleteView

app_name = 'artigos'

urlpatterns = [
    path('', ArtigoListView.as_view(), name='artigo-list'),
    path('novo/', ArtigoCreateView.as_view(), name='artigo-create'),
    path('<slug:slug>/', ArtigoDetailView.as_view(), name='artigo-detail'),
    path('<slug:slug>/editar/', ArtigoUpdateView.as_view(), name='artigo-update'),
    path('<slug:slug>/apagar/', ArtigoDeleteView.as_view(), name='artigo-delete'),
]
