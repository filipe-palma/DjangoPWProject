from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import MagicLink
from django.contrib.auth.models import User
from django.utils import timezone
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
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            messages.error(request, 'Credenciais inválidas.')

    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'autenticacao/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Especificar o backend ao fazer login
            user_auth = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user_auth:
                login(request, user_auth)  # Este usuário já tem o backend configurado
                messages.success(request, 'Conta criada com sucesso!')
                return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'autenticacao/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('/autenticacao/login/')

@login_required
def profile_view(request):
    return render(request, 'autenticacao/profile.html')

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

        # Autenticar o usuário explicitamente antes de fazer login
        backend = 'django.contrib.auth.backends.ModelBackend'
        user.backend = backend

        # Login do usuário
        login(request, user)

        messages.success(request, 'Login realizado com sucesso via link mágico!')
        return redirect('/')

    except MagicLink.DoesNotExist:
        messages.error(request, 'Link mágico inválido.')
        return redirect('/autenticacao/login/')