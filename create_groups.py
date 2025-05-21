#!/usr/bin/env python
import os
import django
import sys

"""
Script para configurar os grupos de usuários e suas permissões no sistema:

1. Gestores: Podem gerenciar projetos e tecnologias do portfólio, além de gerenciar usuários.
   - Têm acesso total (CRUD) a projetos e tecnologias
   - Podem apenas visualizar artigos, comentários e avaliações
   - Podem gerenciar usuários do sistema

2. Autores: Podem gerenciar artigos e moderar comentários.
   - Têm acesso total (CRUD) a artigos, comentários e avaliações
   - Podem visualizar projetos e tecnologias, mas não editá-los
   - Não podem gerenciar usuários do sistema

3. Usuários Default: Podem apenas visualizar conteúdo e fazer comentários/avaliações.
   - Podem visualizar todo o conteúdo
   - Podem adicionar comentários e avaliações (sujeitos à aprovação)
   - Não podem editar nenhum tipo de conteúdo
"""

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
        
        # Criar grupo de Autores
        autores_group, created_autores = Group.objects.get_or_create(name="Autores")
        print(f"Autores group {'created' if created_autores else 'already exists'}")
        
        # Criar grupo de Usuários Default
        usuarios_default_group, created_usuarios = Group.objects.get_or_create(name="Usuários Default")
        print(f"Usuários Default group {'created' if created_usuarios else 'already exists'}")
        
        print("Getting content types for models...")
        # Obter todos os ContentTypes dos modelos relevantes
        artigo_content_type = ContentType.objects.get_for_model(Artigo)
        comentario_content_type = ContentType.objects.get_for_model(Comentario)
        avaliacao_content_type = ContentType.objects.get_for_model(Avaliacao)
        user_content_type = ContentType.objects.get_for_model(User)
        
        # Obter ContentTypes para os modelos de portfolio
        from portfolio.models import Projeto, Tecnologia
        projeto_content_type = ContentType.objects.get_for_model(Projeto)
        tecnologia_content_type = ContentType.objects.get_for_model(Tecnologia)
        print("Content types retrieved successfully")
        
        print("Setting up permissions...")
        # Permissões para Gestores - Podem editar projetos, mas não artigos
        gestores_permissions = [
            # Projetos - CRUD completo
            Permission.objects.get(codename='add_projeto', content_type=projeto_content_type),
            Permission.objects.get(codename='change_projeto', content_type=projeto_content_type),
            Permission.objects.get(codename='delete_projeto', content_type=projeto_content_type),
            Permission.objects.get(codename='view_projeto', content_type=projeto_content_type),
            
            # Tecnologias - CRUD completo
            Permission.objects.get(codename='add_tecnologia', content_type=tecnologia_content_type),
            Permission.objects.get(codename='change_tecnologia', content_type=tecnologia_content_type),
            Permission.objects.get(codename='delete_tecnologia', content_type=tecnologia_content_type),
            Permission.objects.get(codename='view_tecnologia', content_type=tecnologia_content_type),
            
            # Artigos, Comentários, Avaliações - Apenas visualização
            Permission.objects.get(codename='view_artigo', content_type=artigo_content_type),
            Permission.objects.get(codename='view_comentario', content_type=comentario_content_type),
            Permission.objects.get(codename='view_avaliacao', content_type=avaliacao_content_type),
            
            # Usuários - Permissões para gerenciar usuários
            Permission.objects.get(codename='add_user', content_type=user_content_type),
            Permission.objects.get(codename='change_user', content_type=user_content_type),
            Permission.objects.get(codename='view_user', content_type=user_content_type),
        ]
        
        # Permissões para Autores - Podem editar artigos, mas não projetos
        autores_permissions = [
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
            
            # Projetos, Tecnologias - Apenas visualização
            Permission.objects.get(codename='view_projeto', content_type=projeto_content_type),
            Permission.objects.get(codename='view_tecnologia', content_type=tecnologia_content_type),
        ]
        
        # Permissões para Usuários Default - Apenas comentar/avaliar, sem editar nada
        usuarios_default_permissions = [
            # Artigos - Apenas visualização
            Permission.objects.get(codename='view_artigo', content_type=artigo_content_type),
            
            # Comentários - Adicionar e visualizar, mas não editar ou excluir
            Permission.objects.get(codename='add_comentario', content_type=comentario_content_type),
            Permission.objects.get(codename='view_comentario', content_type=comentario_content_type),
            
            # Avaliações - Adicionar e visualizar, mas não editar ou excluir
            Permission.objects.get(codename='add_avaliacao', content_type=avaliacao_content_type),
            Permission.objects.get(codename='view_avaliacao', content_type=avaliacao_content_type),
            
            # Projetos, Tecnologias - Apenas visualização
            Permission.objects.get(codename='view_projeto', content_type=projeto_content_type),
            Permission.objects.get(codename='view_tecnologia', content_type=tecnologia_content_type),
        ]
        
        print("Clearing existing permissions...")
        # Limpar permissões existentes e adicionar as novas
        gestores_group.permissions.clear()
        autores_group.permissions.clear()
        usuarios_default_group.permissions.clear()
        
        print("Adding new permissions to groups...")
        gestores_group.permissions.add(*gestores_permissions)
        autores_group.permissions.add(*autores_permissions)
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
            
        # Criar ou obter um usuário gestor
        gestor_username = 'gestor'
        if not User.objects.filter(username=gestor_username).exists():
            gestor_user = User.objects.create_user(
                username=gestor_username,
                email='gestor@example.com',
                password='gestorpassword',
                first_name='Gestor',
                last_name='Projetos'
            )
            print(f"Usuário '{gestor_username}' criado com sucesso!")
        else:
            gestor_user = User.objects.get(username=gestor_username)
            
        # Adicionar usuário ao grupo de Gestores
        gestor_user.groups.clear()
        gestor_user.groups.add(gestores_group)
        print(f"Usuário '{gestor_username}' adicionado ao grupo de Gestores!")
        
        # Criar ou obter um usuário autor
        autor_username = 'autor'
        if not User.objects.filter(username=autor_username).exists():
            autor_user = User.objects.create_user(
                username=autor_username,
                email='autor@example.com',
                password='autorpassword',
                first_name='Autor',
                last_name='Artigos'
            )
            print(f"Usuário '{autor_username}' criado com sucesso!")
        else:
            autor_user = User.objects.get(username=autor_username)
            
        # Adicionar usuário ao grupo de Autores
        autor_user.groups.clear()
        autor_user.groups.add(autores_group)
        print(f"Usuário '{autor_username}' adicionado ao grupo de Autores!")
            
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
