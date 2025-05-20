from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjetoForm, TecnologiaForm
from datetime import datetime
from .models import Projeto, Tecnologia
from django.contrib.auth.decorators import login_required

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

@login_required
def criar_projeto(request):
    form = ProjetoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/form_projeto.html', {'form': form})

@login_required
def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, pk=id)
    form = ProjetoForm(request.POST or None, instance=projeto)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/form_projeto.html', {'form': form})

@login_required
def apagar_projeto(request, id):
    projeto = get_object_or_404(Projeto, pk=id)
    if request.method == 'POST':
        projeto.delete()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/confirmar_apagar.html', {'obj': projeto})

@login_required
def criar_tecnologia(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/form_tecnologia.html', {'form': form, 'novo': True})

@login_required
def editar_tecnologia(request, id):
    tech = get_object_or_404(Tecnologia, pk=id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tech)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/form_tecnologia.html', {'form': form, 'novo': False})

@login_required
def apagar_tecnologia(request, id):
    tech = get_object_or_404(Tecnologia, pk=id)
    if request.method == 'POST':
        tech.delete()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/confirmar_apagar.html', {'obj': tech})