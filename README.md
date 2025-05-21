# Portfólio Moderno com Django

Este projeto é uma aplicação web de portfólio pessoal desenvolvida com Django, com um design moderno, interativo e responsivo.

## Características Principais

- **Design Moderno e Interativo**: Interface completamente redesenhada usando Bootstrap 5 e CSS personalizado
- **Tema Claro/Escuro**: Alternância entre temas claro e escuro com persistência de preferência
- **Animações**: Efeitos de animação ao scroll e interações usando AOS (Animate on Scroll) e CSS
- **Layout Responsivo**: Design adaptável a todos os tamanhos de tela e dispositivos
- **Gerenciamento de Portfolio**: Sistema completo para adicionar, editar e remover projetos e tecnologias
- **Autenticação de Usuários**: Sistema de login, registro e gerenciamento de perfis
- **Sistema de Grupos de Usuários**: Controle de acesso baseado em grupos com permissões específicas

## Sistema de Grupos de Usuários

O projeto implementa um sistema de controle de acesso baseado em três grupos de usuários:

1. **Gestores**: Podem gerenciar projetos e tecnologias do portfólio, além de gerenciar usuários.
   - Permissões: CRUD completo de projetos e tecnologias, visualização de artigos/comentários/avaliações, gestão de usuários.

2. **Autores**: Podem gerenciar artigos e moderar comentários.
   - Permissões: CRUD completo de artigos, aprovação/exclusão de comentários e avaliações, visualização de projetos.

3. **Usuários Default**: Podem apenas visualizar conteúdo e fazer comentários/avaliações em artigos.
   - Permissões: Visualização de todo o conteúdo, adição de comentários e avaliações (sujeitos à aprovação).

### Restrições de Segurança

O sistema implementa várias restrições de segurança:

#### Restrição para Gerenciamento de Grupos

- **Apenas superusers** podem alterar os grupos aos quais outros usuários pertencem
- Outros usuários, incluindo Gestores, podem ver e editar informações básicas dos usuários, mas não podem mudar seus grupos
- Esta restrição é implementada tanto no backend (controle de permissões) quanto no frontend (interface desabilitada)
- Os formulários de edição de usuário mostram mensagens de aviso apropriadas para não-superusers

#### Restrição de Botões de Edição

- Os botões de edição e exclusão só aparecem para usuários com as respectivas permissões
- Gestores: podem ver botões de edição relacionados a projetos e tecnologias
- Autores: podem ver botões de edição relacionados a artigos
- Usuários Default: não veem nenhum botão de edição
- Superusers: têm acesso a todos os botões de edição

Esta segregação de funções garante que cada tipo de usuário tenha acesso apenas às funcionalidades relevantes para seu papel no sistema, com controle adicional sobre a atribuição de permissões.

## Tecnologias Utilizadas

- **Backend**: Django, Python, SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Bibliotecas JS**: AOS, Font Awesome
- **Ferramentas**: Git, VSCode

## Estrutura do Projeto

```
portfolio/
├── templates/         # Templates HTML
│   ├── base.html      # Template base com a estrutura principal
│   ├── index.html     # Página inicial
│   ├── projetos.html  # Lista de projetos
│   ├── tecnologias.html # Lista de tecnologias
│   └── ...            # Outras páginas
├── models.py          # Modelos de dados
├── views.py           # Views para processar requisições
├── urls.py            # Configuração de URLs
└── forms.py           # Formulários para interação com o usuário
```

## Melhorias de Design Implementadas

1. **Interface Moderna**: Layout limpo e moderno com cards, bordas arredondadas e sombras sutis
2. **Tema Claro/Escuro**: Sistema de temas com variáveis CSS e persistência via localStorage
3. **Animações**: Efeitos de fade, slide e zoom durante a navegação e interação 
4. **Cards Interativos**: Efeitos de hover e transições em cards de projetos e tecnologias
5. **Navegação Aprimorada**: Menu de navegação com ícones e indicadores visuais
6. **Footer Informativo**: Rodapé estruturado com links úteis e informações de contato
7. **Botões Estilizados**: Botões com efeitos de hover e ícones para melhor usabilidade
8. **Timeline e Barras de Progresso**: Elementos visuais para apresentar informações de forma mais dinâmica
9. **Hero Sections**: Seções de destaque para cada página principal
10. **Modal para Detalhes**: Visualização de detalhes de projetos em modais interativos

## Instruções de Instalação

1. Clone o repositório:
```bash
git clone https://github.com/filipe-palma/DjangoPWProject
cd DjangoPWProject
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações:
```bash
python manage.py migrate
```

4. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

5. Acesse http://127.0.0.1:8000/ no seu navegador

## Autor

Filipe Palma - [filipepalma9@hotmail.com](mailto:filipepalma9@hotmail.com)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
