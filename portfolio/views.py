from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjetoForm, TecnologiaForm, AreaInteresseForm
from datetime import datetime
from .models import Projeto, Tecnologia, AreaInteresse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden

# Função para verificar se o usuário é um gestor ou superusuário
def is_gestor(user):
    return user.is_superuser or user.groups.filter(name='Gestores').exists()

def index_view(request):
    return render(request, "portfolio/index.html", {"data_atual": datetime.now()})

def sobre_view(request):
    return render(request, "portfolio/sobre.html")

def interesses_view(request):
    return render(request, "portfolio/interesses.html")

def projetos_view(request):
    projetos = Projeto.objects.all().prefetch_related('tecnologias', 'imagens')
    return render(request, "portfolio/projetos.html", {"projetos": projetos})

def tecnologias_view(request):
    techs = Tecnologia.objects.all().prefetch_related('projeto_set')
    return render(request, "portfolio/tecnologias.html", {"techs": techs})

def apresentacao_view(request):
    return render(request, "portfolio/apresentacao.html")

def cv_view(request):
    return render(request, "portfolio/cv.html")

def areainteresse_view(request):
    areainteresse = AreaInteresse.objects.all()
    return render(request, "portfolio/areainteresse.html", {"areainteresse": areainteresse})



@login_required
@user_passes_test(is_gestor)
def criar_projeto(request):
    form = ProjetoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Projeto criado com sucesso!")
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/form_projeto.html', {'form': form})

@login_required
@user_passes_test(is_gestor)
def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, pk=id)
    form = ProjetoForm(request.POST or None, instance=projeto)
    if form.is_valid():
        form.save()
        messages.success(request, "Projeto atualizado com sucesso!")
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/form_projeto.html', {'form': form})

@login_required
@user_passes_test(is_gestor)
def apagar_projeto(request, id):
    projeto = get_object_or_404(Projeto, pk=id)
    if request.method == 'POST':
        projeto.delete()
        messages.success(request, "Projeto removido com sucesso!")
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/confirmar_apagar.html', {'obj': projeto})

@login_required
@user_passes_test(is_gestor)
def criar_tecnologia(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Tecnologia criada com sucesso!")
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/form_tecnologia.html', {'form': form, 'novo': True})

@login_required
@user_passes_test(is_gestor)
def editar_tecnologia(request, id):
    tech = get_object_or_404(Tecnologia, pk=id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tech)
    if form.is_valid():
        form.save()
        messages.success(request, "Tecnologia atualizada com sucesso!")
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/form_tecnologia.html', {'form': form, 'novo': False})

@login_required
@user_passes_test(is_gestor)
def editar_areainteresse(request, id):
    areainteresse = get_object_or_404(AreaInteresse, pk=id)
    form = AreaInteresseForm(request.POST or None, request.FILES or None, instance=areainteresse)
    if form.is_valid():
        form.save()
        messages.success(request, "Area de Interesse atualizada com sucesso!")
        return redirect('portfolio:areainteresse')
    return render(request, 'portfolio/form_areainteresse.html', {'form': form, 'novo': False})

@login_required
@user_passes_test(is_gestor)
def apagar_tecnologia(request, id):
    tech = get_object_or_404(Tecnologia, pk=id)
    if request.method == 'POST':
        tech.delete()
        messages.success(request, "Tecnologia removida com sucesso!")
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/confirmar_apagar.html', {'obj': tech})