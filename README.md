# Sistema de Gestão Escolar

Sistema de gestão escolar desenvolvido em Django para gerenciar alunos, professores e administração.

## Estrutura do Projeto

```
escola/
│── manage.py
│── escola/               # Configurações principais
│── apps/
│    ├── accounts/         # Usuários, autenticação, perfis e seleção de unidade
│    ├── core/             # Modelos base, utilidades
│    ├── alunos/           # Funcionalidades do aluno
│    ├── professores/      # Funcionalidades do professor
│    ├── administracao/    # Funcionalidades da administração
│    └── relatorios/       # Relatórios e exportações
│── requirements.txt
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. Execute as migrações:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Configure dados iniciais:
   ```bash
   python manage.py setup_initial_data
   ```

7. Execute o servidor:
   ```bash
   python manage.py runserver
   ```

## Configuração Inicial

Após executar `setup_initial_data`, você terá:

- **Usuário Administrador:**
  - Username: `admin`
  - Password: `admin123`

- **Unidades Escolares de Exemplo:**
  - Escola Municipal João da Silva
  - Escola Municipal Maria Santos

- **Disciplinas Básicas:**
  - Matemática, Português, História, Geografia, Ciências, etc.

- **Turmas de Exemplo:**
  - 1º, 2º e 3º anos (manhã e tarde)

## Endpoints da API

### Autenticação
- `POST /api/accounts/register/` - Registro de usuários
- `POST /api/accounts/login/` - Login com JWT
- `POST /api/accounts/logout/` - Logout
- `POST /api/accounts/token/refresh/` - Renovar token JWT

### Unidades Escolares
- `GET /api/accounts/unidades/` - Listar unidades ativas
- `GET /api/accounts/unidades/{id}/` - Detalhes da unidade

### Perfil do Usuário
- `GET /api/accounts/profile/` - Ver perfil
- `PUT /api/accounts/profile/` - Atualizar perfil
- `POST /api/accounts/change-password/` - Alterar senha

## Apps

### accounts
- Gerenciamento de usuários
- Autenticação
- Perfis de usuário
- Seleção de unidade escolar

### core
- Modelos base
- Utilitários comuns
- Configurações compartilhadas

### alunos
- Cadastro de alunos
- Histórico escolar
- Notas e frequência

### professores
- Cadastro de professores
- Disciplinas
- Turmas

### administracao
- Gestão administrativa
- Configurações do sistema
- Controle de acesso

### relatorios
- Geração de relatórios
- Exportação de dados
- Estatísticas

## 📚 Documentação

- **Guia de Instalação:** `INSTALACAO.md` - Instruções detalhadas de instalação
- **Quick Start:** `QUICK_START.md` - Setup rápido para desenvolvedores
- **Windows Setup:** `WINDOWS_SETUP.md` - Guia específico para Windows
- **API Documentation:** `API_DOCUMENTATION.md` - Documentação completa da API
- **Database Configuration:** `db_config.md` - Configuração do banco de dados
- **Funcionalidades:** `FUNCIONALIDADES.md` - Resumo das funcionalidades implementadas
- **Visão Geral:** `PROJETO.md` - Visão executiva do projeto

## Tecnologias Utilizadas

- Django 4.2+
- Django REST Framework
- SimpleJWT (Autenticação)
- SQLite (desenvolvimento) / PostgreSQL (produção)
- Python 3.8+

## Licença

Este projeto está sob a licença MIT.
