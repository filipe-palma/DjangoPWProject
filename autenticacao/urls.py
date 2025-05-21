from django.urls import path
from . import views
from . import admin_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm

# Classe personalizada para o formulário de confirmação de senha
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('magic-link/', views.magic_link_view, name='magic_link'),
    path('magic-link-sent/', views.magic_link_sent_view, name='magic_link_sent'),
    path('verify-magic-link/<uuid:token>/', views.verify_magic_link_view, name='verify_magic_link'),
    
    # Recuperação de senha
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='autenticacao/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='autenticacao/password_reset_confirm.html',
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='autenticacao/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Gerenciamento de usuários (apenas para gestores)
    path('admin/users/', admin_views.user_list, name='user_list'),
    path('admin/users/<int:user_id>/edit/', admin_views.user_edit, name='user_edit'),
]