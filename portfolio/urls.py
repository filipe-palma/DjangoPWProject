from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('interesses/', views.interesses_view, name='interesses'),
    path('projetos/', views.projetos_view, name='projetos'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('apresentacao/', views.apresentacao_view, name='apresentacao'),
    path('cv/', views.cv_view, name='cv'),
    path('projetos/novo/', views.criar_projeto, name='criar_projeto'),
    path('projetos/editar/<int:id>/', views.editar_projeto, name='editar_projeto'),
    path('projetos/apagar/<int:id>/', views.apagar_projeto, name='apagar_projeto'),
    path('tecnologias/novo/', views.criar_tecnologia, name='criar_tecnologia'),
    path('tecnologias/editar/<int:id>/', views.editar_tecnologia, name='editar_tecnologia'),
    path('tecnologias/apagar/<int:id>/', views.apagar_tecnologia, name='apagar_tecnologia'),
    path('areainteresse/', views.areainteresse_view, name='areainteresse'),
    
    # AJAX Disciplinas URLs
    path('ajax/disciplinas/', views.ajax_listar_disciplinas, name='ajax_listar_disciplinas'),
    path('ajax/disciplinas/criar/', views.ajax_criar_disciplina, name='ajax_criar_disciplina'),
    path('ajax/disciplinas/editar/<int:id>/', views.ajax_editar_disciplina, name='ajax_editar_disciplina'),
    path('ajax/disciplinas/apagar/<int:id>/', views.ajax_apagar_disciplina, name='ajax_apagar_disciplina'),
    
    # Imagens de Projeto URLs
    path('projetos/<int:projeto_id>/imagens/', views.imagens_projeto_view, name='imagens_projeto'),
    path('projetos/<int:projeto_id>/imagens/nova/', views.criar_imagem_projeto, name='criar_imagem_projeto'),
    path('projetos/imagens/apagar/<int:id>/', views.apagar_imagem_projeto, name='apagar_imagem_projeto'),
    
    # Extras URLs
    path('projetos/<int:projeto_id>/extras/', views.criar_editar_extras, name='criar_editar_extras'),
    path('projetos/<int:projeto_id>/extras/apagar/', views.apagar_extras, name='apagar_extras'),
]