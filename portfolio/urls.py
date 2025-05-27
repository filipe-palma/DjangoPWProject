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
]