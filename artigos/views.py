from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import Artigo, Comentario, Avaliacao
from .forms import ArtigoForm, ComentarioForm, AvaliacaoForm

class ArtigoListView(generic.ListView):
    model = Artigo
    template_name = 'artigos/artigo_list.html'
    context_object_name = 'artigos'
    paginate_by = 10

class ArtigoDetailView(generic.DetailView):
    model = Artigo
    template_name = 'artigos/artigo_detail.html'
    context_object_name = 'artigo'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comentarios'] = self.object.comentarios.filter(aprovado=True)
        ctx['form_comentario'] = ComentarioForm()
        ctx['avaliacoes'] = self.object.avaliacoes.all()
        ctx['form_avaliacao'] = AvaliacaoForm()
        
        # Adicionar informações sobre permissões para o template
        user = self.request.user
        # Somente Autores e superusuários podem aprovar comentários e editar/excluir artigos
        ctx['pode_aprovar_comentarios'] = user.is_superuser or user.has_perm('artigos.change_comentario')
        ctx['pode_editar_artigo'] = user.is_superuser or user.has_perm('artigos.change_artigo')
        ctx['pode_excluir_artigo'] = user.is_superuser or user.has_perm('artigos.delete_artigo')
        ctx['pode_gerenciar_usuarios'] = user.is_superuser or user.has_perm('auth.change_user')
        ctx['is_autor'] = user.groups.filter(name='Autores').exists() if user.is_authenticated else False
        ctx['is_gestor'] = user.groups.filter(name='Gestores').exists() if user.is_authenticated else False
        ctx['is_superuser'] = user.is_superuser if user.is_authenticated else False
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para comentar ou avaliar artigos.')
            return redirect('autenticacao:login')
            
        if 'submit_comentario' in request.POST:
            if not request.user.has_perm('artigos.add_comentario'):
                messages.error(request, 'Você não tem permissão para adicionar comentários.')
                return redirect(self.object)
                
            form = ComentarioForm(request.POST)
            if form.is_valid():
                com = form.save(commit=False)
                com.artigo = self.object
                com.usuario = request.user if request.user.is_authenticated else None
                
                # Set nome to username, email fields from user
                com.nome = request.user.username
                com.email = request.user.email
                
                # Comentários de autores são aprovados automaticamente
                if request.user.groups.filter(name='Autores').exists():
                    com.aprovado = True
                
                com.save()
                messages.success(request, 'Seu comentário foi enviado com sucesso' + 
                                (' e aprovado automaticamente.' if com.aprovado else ' e aguarda aprovação.'))
                return redirect(self.object)
            else:
                # Form is invalid - show error messages
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                # Re-render the page with the form errors
                ctx = self.get_context_data()
                ctx['form_comentario'] = form 
                # Keep the avaliação form fresh
                ctx['form_avaliacao'] = AvaliacaoForm()
                return self.render_to_response(ctx)
            
        if 'submit_avaliacao' in request.POST:
            if not request.user.has_perm('artigos.add_avaliacao'):
                messages.error(request, 'Você não tem permissão para adicionar avaliações.')
                return redirect(self.object)
                
            form = AvaliacaoForm(request.POST)
            if form.is_valid():
                aval = form.save(commit=False)
                aval.artigo = self.object
                aval.usuario = request.user if request.user.is_authenticated else None
                
                # Set nome to username and email fields from user
                aval.nome = request.user.username
                aval.email = request.user.email
                
                # No comentario field as per requirements
                aval.save()
                messages.success(request, 'Sua avaliação foi enviada com sucesso.')
                return redirect(self.object)
            else:
                # Form is invalid - show error messages
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                # Re-render the page with the form errors
                ctx = self.get_context_data()
                ctx['form_avaliacao'] = form
                # Keep the comment form fresh
                ctx['form_comentario'] = ComentarioForm()
                return self.render_to_response(ctx)
            
        return super().get(request, *args, **kwargs)

class ArtigoCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Artigo
    form_class = ArtigoForm
    template_name = 'artigos/artigo_form.html'
    permission_required = 'artigos.add_artigo'
    login_url = '/autenticacao/login/'
    
    def get_success_url(self):
        return reverse('artigos:artigo-detail', args=[self.object.slug])
        
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para criar artigos. Apenas gestores podem realizar esta operação.')
        return super().handle_no_permission()

class ArtigoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Artigo
    form_class = ArtigoForm
    template_name = 'artigos/artigo_form.html'
    permission_required = 'artigos.change_artigo'
    login_url = '/autenticacao/login/'
    
    def get_success_url(self):
        return reverse('artigos:artigo-detail', args=[self.object.slug])
        
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para editar artigos. Apenas gestores podem realizar esta operação.')
        return super().handle_no_permission()

class ArtigoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Artigo
    template_name = 'artigos/artigo_confirm_delete.html'
    success_url = reverse_lazy('artigos:artigo-list')
    permission_required = 'artigos.delete_artigo'
    login_url = '/autenticacao/login/'
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para excluir artigos. Apenas gestores podem realizar esta operação.')
        return super().handle_no_permission()

class ComentariosListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Comentario
    template_name = 'artigos/comentarios_moderation.html'
    context_object_name = 'comentarios'
    paginate_by = 10
    permission_required = 'artigos.change_comentario'
    login_url = '/autenticacao/login/'
    
    def get_queryset(self):
        filter_param = self.request.GET.get('filter', 'pendente')
        
        if filter_param == 'pendente':
            return Comentario.objects.filter(aprovado=False).order_by('-data_criacao')
        elif filter_param == 'aprovado':
            return Comentario.objects.filter(aprovado=True).order_by('-data_criacao')
        else:  # 'todos'
            return Comentario.objects.all().order_by('-data_criacao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'pendente')
        return context
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para moderar comentários. Esta ação está disponível apenas para gestores.')
        return super().handle_no_permission()

@login_required
@permission_required('artigos.change_comentario', raise_exception=True)
def approve_comment(request, comment_id):
    if request.method == 'POST':
        comentario = get_object_or_404(Comentario, pk=comment_id)
        comentario.aprovado = True
        comentario.save()
        messages.success(request, f'Comentário de {comentario.nome} foi aprovado com sucesso.')
        
        # Redirecionar para a lista mantendo o filtro atual
        filter_param = request.GET.get('filter', 'pendente')
        return redirect(f"{reverse('artigos:comentarios-moderacao')}?filter={filter_param}")
    
    messages.error(request, 'Método não permitido.')
    return redirect('artigos:comentarios-moderacao')

@login_required
@permission_required('artigos.delete_comentario', raise_exception=True)
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comentario = get_object_or_404(Comentario, pk=comment_id)
        nome = comentario.nome
        comentario.delete()
        messages.success(request, f'Comentário de {nome} foi excluído com sucesso.')
        
        # Redirecionar para a lista mantendo o filtro atual
        filter_param = request.GET.get('filter', 'pendente')
        return redirect(f"{reverse('artigos:comentarios-moderacao')}?filter={filter_param}")
    
    messages.error(request, 'Método não permitido.')
    return redirect('artigos:comentarios-moderacao')
