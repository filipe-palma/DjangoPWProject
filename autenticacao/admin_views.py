from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django import forms

class UserForm(forms.ModelForm):
    GROUP_CHOICES = [
        ('', 'Usuário Default'),
        ('gestor', 'Gestor'),
        ('autor', 'Autor'),
    ]
    
    group_choice = forms.ChoiceField(
        choices=GROUP_CHOICES, 
        required=False, 
        label='Grupo do Usuário',
        help_text='Apenas superusers podem alterar os grupos',
        disabled=True  # Campo desativado por padrão
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'group_choice']
        
    def __init__(self, *args, **kwargs):
        # O request é passado como argumento adicional
        self.request = kwargs.pop('request', None)
        super(UserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['group_choice'].widget.attrs.update({'class': 'form-select'})
        
        # Habilitar o campo de grupo apenas para superusers
        if self.request and self.request.user.is_superuser:
            self.fields['group_choice'].disabled = False
            self.fields['group_choice'].help_text = 'Escolha o grupo principal do usuário'
        
        # Verificar o grupo atual do usuário
        if self.instance and self.instance.pk:
            if self.instance.groups.filter(name='Gestores').exists():
                self.fields['group_choice'].initial = 'gestor'
            elif self.instance.groups.filter(name='Autores').exists():
                self.fields['group_choice'].initial = 'autor'
            else:
                self.fields['group_choice'].initial = ''

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
    autores_group = Group.objects.get(name='Autores')
    usuarios_default_group = Group.objects.get(name='Usuários Default')
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj, request=request)
        if form.is_valid():
            user = form.save()
            
            # Apenas superusers podem alterar grupos
            if request.user.is_superuser:
                # Gerenciar grupos com base na seleção do form
                group_choice = form.cleaned_data.get('group_choice')
                
                # Limpar todos os grupos primeiro
                user.groups.clear()
                
                # Adicionar ao grupo apropriado
                if group_choice == 'gestor':
                    user.groups.add(gestores_group)
                elif group_choice == 'autor':
                    user.groups.add(autores_group)
                else:  # Default
                    user.groups.add(usuarios_default_group)
                
                messages.success(request, f'Usuário {user.username} foi atualizado com sucesso, incluindo seu grupo.')
            else:
                messages.success(request, f'Usuário {user.username} foi atualizado com sucesso. Apenas superusers podem alterar grupos.')
            
            return redirect('user_list')
    else:
        form = UserForm(instance=user_obj, request=request)
    
    return render(request, 'autenticacao/user_edit.html', {
        'form': form,
        'user_obj': user_obj
    })
