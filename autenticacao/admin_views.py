from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django import forms

class UserForm(forms.ModelForm):
    is_gestor = forms.BooleanField(required=False, label='É Gestor')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_gestor'].widget.attrs.update({'class': 'form-check-input'})
        
        # Verificar se o usuário é gestor
        if self.instance and self.instance.pk:
            self.fields['is_gestor'].initial = self.instance.groups.filter(name='Gestores').exists()

@login_required
@permission_required('auth.view_user', raise_exception=True)
def user_list(request):
    users = User.objects.all().order_by('username')
    
    # Paginação
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'autenticacao/user_list.html', {
        'page_obj': page_obj,
        'users': page_obj.object_list,
    })

@login_required
@permission_required('auth.change_user', raise_exception=True)
def user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    gestores_group = Group.objects.get(name='Gestores')
    usuarios_default_group = Group.objects.get(name='Usuários Default')
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save()
            
            # Gerenciar grupos
            is_gestor = form.cleaned_data.get('is_gestor')
            if is_gestor:
                # Adicionar ao grupo de gestores se não estiver
                if not user.groups.filter(name='Gestores').exists():
                    user.groups.add(gestores_group)
                # Remover do grupo de usuários padrão se estiver
                if user.groups.filter(name='Usuários Default').exists():
                    user.groups.remove(usuarios_default_group)
            else:
                # Remover do grupo de gestores se estiver
                if user.groups.filter(name='Gestores').exists():
                    user.groups.remove(gestores_group)
                # Adicionar ao grupo de usuários padrão se não estiver
                if not user.groups.filter(name='Usuários Default').exists():
                    user.groups.add(usuarios_default_group)
            
            messages.success(request, f'Usuário {user.username} foi atualizado com sucesso.')
            return redirect('user_list')
    else:
        form = UserForm(instance=user_obj)
    
    return render(request, 'autenticacao/user_edit.html', {
        'form': form,
        'user_obj': user_obj
    })
