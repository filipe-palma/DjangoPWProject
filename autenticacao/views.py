from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import MagicLink
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
import uuid

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Especificar o backend explicitamente
        user = authenticate(
            request,
            username=username,
            password=password,
            backend='django.contrib.auth.backends.ModelBackend'
        )

        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', '/portfolio/index/')
            return redirect(next_page)
        else:
            messages.error(request, 'Credenciais inválidas.')

    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'autenticacao/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            # Adicionar o usuário ao grupo "Usuários Default"
            from django.contrib.auth.models import Group
            usuarios_default_group = Group.objects.get(name="Usuários Default")
            user.groups.add(usuarios_default_group)
            
            # Especificar o backend ao fazer login
            user_auth = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user_auth:
                login(request, user_auth)  # Este usuário já tem o backend configurado
                messages.success(request, 'Conta criada com sucesso! Você foi adicionado ao grupo de Usuários Default.')
                return redirect('/portfolio/index/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'autenticacao/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('/autenticacao/login/')

@login_required
def profile_view(request):
    user = request.user
    
    # Get user's groups
    groups = user.groups.all()
    
    # Get permissions organized by model
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    
    user_permissions = user.get_all_permissions()
    
    # Organize permissions by app/model for better readability
    organized_permissions = {}
    for perm in user_permissions:
        app_label, codename = perm.split('.', 1)
        if app_label not in organized_permissions:
            organized_permissions[app_label] = []
        organized_permissions[app_label].append(codename)
    
    context = {
        'user': user,
        'groups': groups,
        'is_gestor': user.groups.filter(name='Gestores').exists(),
        'is_default': user.groups.filter(name='Usuários Default').exists(),
        'pode_gerenciar_usuarios': user.has_perm('auth.change_user'),
        'organized_permissions': organized_permissions,
    }
    return render(request, 'autenticacao/profile.html', context)

def magic_link_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificar se o usuário existe
        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            messages.error(request, 'Não existe conta com este email.')
            return render(request, 'autenticacao/magic_link.html')

        # Criar o token de link mágico
        magic_link = MagicLink.objects.create(
            email=email,
            token=uuid.uuid4(),
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )

        # Construir o link completo
        magic_url = request.build_absolute_uri(f'/autenticacao/verify-magic-link/{magic_link.token}/')

        # Enviar email
        send_mail(
            'Seu Link Mágico de Acesso',
            f'Clique no link a seguir para acessar o sistema: {magic_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(request, 'Link mágico enviado para seu email.')
        return redirect('/autenticacao/magic-link-sent/')

    return render(request, 'autenticacao/magic_link.html')

def magic_link_sent_view(request):
    return render(request, 'autenticacao/magic_link_sent.html')

def verify_magic_link_view(request, token):
    try:
        # Tentar encontrar o token
        magic_link = MagicLink.objects.get(token=token)

        # Verificar se o token é válido
        if not magic_link.is_valid():
            messages.error(request, 'Link mágico expirado ou já utilizado.')
            return redirect('/autenticacao/login/')

        # Marcar token como usado
        magic_link.is_used = True
        magic_link.save()

        # Buscar ou criar usuário
        user, created = User.objects.get_or_create(
            email=magic_link.email,
            defaults={'username': magic_link.email.split('@')[0]}
        )

        # Se um usuário foi criado, defina uma senha aleatória
        if created:
            random_password = User.objects.make_random_password()
            user.set_password(random_password)
            user.save()
            
            # Adicionar o usuário recém-criado ao grupo "Usuários Default"
            from django.contrib.auth.models import Group
            usuarios_default_group = Group.objects.get(name="Usuários Default")
            user.groups.add(usuarios_default_group)

        # Autenticar o usuário explicitamente antes de fazer login
        backend = 'django.contrib.auth.backends.ModelBackend'
        user.backend = backend        # Login do usuário
        login(request, user)
        messages.success(request, 'Login realizado com sucesso via link mágico!')
        return redirect('/portfolio/index/')

    except MagicLink.DoesNotExist:
        messages.error(request, 'Link mágico inválido.')
        return redirect('/autenticacao/login/')

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name='autenticacao/password_reset_email.html',
                subject_template_name='autenticacao/password_reset_subject.txt',
            )
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    
    # Adicionar classes aos campos do formulário
    form.fields['email'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Digite seu endereço de email'
    })
    
    return render(request, 'autenticacao/password_reset_form.html', {
        'form': form
    })