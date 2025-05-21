#!/usr/bin/env python
import os
import django
import sys

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

try:
    django.setup()
    print("Django setup completed successfully.")
except Exception as e:
    print(f"Error in Django setup: {e}")
    sys.exit(1)

try:
    from django.contrib.auth.models import Group, Permission, User
    from django.contrib.contenttypes.models import ContentType
    from artigos.models import Artigo, Comentario, Avaliacao
    print("Imports completed successfully.")
except Exception as e:
    print(f"Error in imports: {e}")
    sys.exit(1)

# Função para criar grupos e adicionar permissões
def setup_groups_and_permissions():
    try:
        print("Creating or getting groups...")
        # Criar grupo de Gestores
        gestores_group, created_gestores = Group.objects.get_or_create(name="Gestores")
        print(f"Gestores group {'created' if created_gestores else 'already exists'}")
        
        # Criar grupo de Usuários Default
        usuarios_default_group, created_usuarios = Group.objects.get_or_create(name="Usuários Default")
        print(f"Usuários Default group {'created' if created_usuarios else 'already exists'}")
        
        print("Getting content types for models...")
        # Obter todos os ContentTypes dos modelos relevantes
        artigo_content_type = ContentType.objects.get_for_model(Artigo)
        comentario_content_type = ContentType.objects.get_for_model(Comentario)
        avaliacao_content_type = ContentType.objects.get_for_model(Avaliacao)
        user_content_type = ContentType.objects.get_for_model(User)
        print("Content types retrieved successfully")
        
        print("Setting up permissions...")
        # Permissões para Gestores
        gestores_permissions = [
            # Artigos - CRUD completo
            Permission.objects.get(codename='add_artigo', content_type=artigo_content_type),
            Permission.objects.get(codename='change_artigo', content_type=artigo_content_type),
            Permission.objects.get(codename='delete_artigo', content_type=artigo_content_type),
            Permission.objects.get(codename='view_artigo', content_type=artigo_content_type),
            
            # Comentários - CRUD completo com ênfase em moderação
            Permission.objects.get(codename='add_comentario', content_type=comentario_content_type),
            Permission.objects.get(codename='change_comentario', content_type=comentario_content_type),
            Permission.objects.get(codename='delete_comentario', content_type=comentario_content_type),
            Permission.objects.get(codename='view_comentario', content_type=comentario_content_type),
            
            # Avaliações - CRUD completo
            Permission.objects.get(codename='add_avaliacao', content_type=avaliacao_content_type),
            Permission.objects.get(codename='change_avaliacao', content_type=avaliacao_content_type),
            Permission.objects.get(codename='delete_avaliacao', content_type=avaliacao_content_type),
            Permission.objects.get(codename='view_avaliacao', content_type=avaliacao_content_type),
            
            # Usuários - Permissões para gerenciar usuários
            Permission.objects.get(codename='add_user', content_type=user_content_type),
            Permission.objects.get(codename='change_user', content_type=user_content_type),
            Permission.objects.get(codename='view_user', content_type=user_content_type),
        ]
        
        # Permissões para Usuários Default
        usuarios_default_permissions = [
            # Artigos - Apenas visualização
            Permission.objects.get(codename='view_artigo', content_type=artigo_content_type),
            
            # Comentários - Adicionar e visualizar, mas não editar ou excluir
            Permission.objects.get(codename='add_comentario', content_type=comentario_content_type),
            Permission.objects.get(codename='view_comentario', content_type=comentario_content_type),
            
            # Avaliações - Adicionar e visualizar, mas não editar ou excluir
            Permission.objects.get(codename='add_avaliacao', content_type=avaliacao_content_type),
            Permission.objects.get(codename='view_avaliacao', content_type=avaliacao_content_type),
        ]
        
        print("Clearing existing permissions...")
        # Limpar permissões existentes e adicionar as novas
        gestores_group.permissions.clear()
        usuarios_default_group.permissions.clear()
        
        print("Adding new permissions to groups...")
        gestores_group.permissions.add(*gestores_permissions)
        usuarios_default_group.permissions.add(*usuarios_default_permissions)
        
        print("Grupos e permissões configurados com sucesso!")
        
        # Verificar se existe um superusuário admin e criar um se não existir
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            print("Superusuário 'admin' criado com sucesso!")
            
            # Adicionar este usuário ao grupo de Gestores
            admin_user.groups.add(gestores_group)
            print("Usuário 'admin' adicionado ao grupo de Gestores!")
            
    except Exception as e:
        print(f"Error in setup_groups_and_permissions: {e}")
        raise

if __name__ == "__main__":
    try:
        setup_groups_and_permissions()
        print("Script completed successfully!")
    except Exception as e:
        print(f"Script failed with error: {e}")
        sys.exit(1)
