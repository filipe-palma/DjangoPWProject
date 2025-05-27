from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import JsonResponse
from .forms import ProjetoForm, TecnologiaForm, AreaInteresseForm, DisciplinaForm, ImagemProjetoForm, ExtrasForm
from datetime import datetime
from .models import Projeto, Tecnologia, AreaInteresse, Disciplina, ImagemProjeto, Extras
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

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
    
    # Get all disciplines for the modal
    disciplinas = Disciplina.objects.all()
    
    return render(request, 'portfolio/form_projeto.html', {
        'form': form,
        'disciplinas': disciplinas
    })

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

# Disciplina views
@login_required
@user_passes_test(is_gestor)
def disciplinas_view(request):
    disciplinas = Disciplina.objects.all()
    return render(request, "portfolio/disciplinas.html", {"disciplinas": disciplinas})

@login_required
@user_passes_test(is_gestor)
def criar_disciplina(request):
    form = DisciplinaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Disciplina criada com sucesso!")
        return redirect('portfolio:disciplinas')
    return render(request, 'portfolio/form_disciplina.html', {'form': form, 'novo': True})

@login_required
@user_passes_test(is_gestor)
def editar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, pk=id)
    form = DisciplinaForm(request.POST or None, instance=disciplina)
    if form.is_valid():
        form.save()
        messages.success(request, "Disciplina atualizada com sucesso!")
        return redirect('portfolio:disciplinas')
    return render(request, 'portfolio/form_disciplina.html', {'form': form, 'novo': False})

@login_required
@user_passes_test(is_gestor)
def apagar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, pk=id)
    if request.method == 'POST':
        disciplina.delete()
        messages.success(request, "Disciplina removida com sucesso!")
        return redirect('portfolio:disciplinas')
    return render(request, 'portfolio/confirmar_apagar.html', {'obj': disciplina})

# ImagemProjeto views
@login_required
@user_passes_test(is_gestor)
def imagens_projeto_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    imagens = ImagemProjeto.objects.filter(projeto=projeto)
    return render(request, "portfolio/imagens_projeto.html", {"projeto": projeto, "imagens": imagens})

@login_required
@user_passes_test(is_gestor)
def criar_imagem_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    if request.method == 'POST':
        form = ImagemProjetoForm(request.POST, request.FILES)
        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.projeto = projeto
            imagem.save()
            messages.success(request, "Imagem adicionada com sucesso!")
            return redirect('portfolio:imagens_projeto', projeto_id=projeto_id)
    else:
        form = ImagemProjetoForm(initial={'projeto': projeto})
        # Using forms from the django import we added
        form.fields['projeto'].widget = forms.HiddenInput()
    
    return render(request, 'portfolio/form_imagem.html', {'form': form, 'projeto': projeto})

@login_required
@user_passes_test(is_gestor)
def apagar_imagem_projeto(request, id):
    imagem = get_object_or_404(ImagemProjeto, pk=id)
    projeto_id = imagem.projeto.id
    if request.method == 'POST':
        imagem.delete()
        messages.success(request, "Imagem removida com sucesso!")
        return redirect('portfolio:imagens_projeto', projeto_id=projeto_id)
    return render(request, 'portfolio/confirmar_apagar.html', {'obj': imagem})

# Extras views
@login_required
@user_passes_test(is_gestor)
def criar_editar_extras(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    extras, created = Extras.objects.get_or_create(projeto=projeto)
    
    if request.method == 'POST':
        form = ExtrasForm(request.POST, instance=extras)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações extras atualizadas com sucesso!")
            return redirect('portfolio:editar_projeto', id=projeto_id)
    else:
        form = ExtrasForm(instance=extras)
        form.fields['projeto'].widget = forms.HiddenInput()
    
    return render(request, 'portfolio/form_extras.html', {'form': form, 'projeto': projeto})

@login_required
@user_passes_test(is_gestor)
def apagar_extras(request, projeto_id):
    extras = get_object_or_404(Extras, projeto__id=projeto_id)
    if request.method == 'POST':
        extras.delete()
        messages.success(request, "Informações extras removidas com sucesso!")
        return redirect('portfolio:editar_projeto', id=projeto_id)
    return render(request, 'portfolio/confirmar_apagar.html', {'obj': extras})

# AJAX views for disciplinas
@login_required
@user_passes_test(is_gestor)
@csrf_exempt
def ajax_criar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save()
            return JsonResponse({
                'status': 'success',
                'id': disciplina.id,
                'nome': disciplina.nome,
                'ano': disciplina.ano,
                'semestre': disciplina.semestre,
                'docente': disciplina.docente,
                'moodle_url': disciplina.moodle_url,
                'pagina_uc': disciplina.pagina_uc
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})

@login_required
@user_passes_test(is_gestor)
@csrf_exempt
def ajax_editar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, pk=id)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            disciplina = form.save()
            return JsonResponse({
                'status': 'success',
                'id': disciplina.id,
                'nome': disciplina.nome,
                'ano': disciplina.ano,
                'semestre': disciplina.semestre,
                'docente': disciplina.docente,
                'moodle_url': disciplina.moodle_url,
                'pagina_uc': disciplina.pagina_uc
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})

@login_required
@user_passes_test(is_gestor)
@csrf_exempt
def ajax_apagar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, pk=id)
    if request.method == 'POST':
        disciplina.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})

@login_required
@user_passes_test(is_gestor)
def ajax_listar_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    data = []
    for d in disciplinas:
        data.append({
            'id': d.id,
            'nome': d.nome,
            'ano': d.ano,
            'semestre': d.semestre,
            'docente': d.docente,
            'moodle_url': d.moodle_url,
            'pagina_uc': d.pagina_uc
        })
    return JsonResponse({'disciplinas': data})