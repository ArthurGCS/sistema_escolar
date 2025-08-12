# 🚀 Guia de Instalação e Execução - Sistema de Gestão Escolar

Este guia irá te ajudar a configurar e executar o Sistema de Gestão Escolar localmente em sua máquina.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** (gerenciador de pacotes Python)
- **virtualenv** ou **venv** (para ambientes virtuais)

### Verificando as Instalações

Abra o terminal e execute:

```bash
# Verificar Python
python --version
# ou
python3 --version

# Verificar pip
pip --version

# Verificar Git
git --version
```

## 🛠️ Instalação Passo a Passo

### 1. Clone o Repositório

```bash
# Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd escola
```

### 2. Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv
# ou
python3 -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
# Instalar todas as dependências
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar o arquivo .env com suas configurações
# Use um editor de texto de sua preferência
```

**Conteúdo recomendado para o arquivo `.env`:**

```env
# Configurações do Django
SECRET_KEY=django-insecure-sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações do Banco de Dados (SQLite para desenvolvimento)
# Para PostgreSQL em produção, descomente e configure:
# DB_NAME=escola_db
# DB_USER=escola_user
# DB_PASSWORD=sua-senha
# DB_HOST=localhost
# DB_PORT=5432

# Configurações de Email (opcional)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=seu-email@gmail.com
# EMAIL_HOST_PASSWORD=sua-senha-de-app
# DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

### 5. Configurar Banco de Dados

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate
```

### 6. Configurar Dados Iniciais

```bash
# Executar comando para criar dados iniciais
python manage.py setup_initial_data
```

**Dados que serão criados:**
- Usuário administrador: `admin` / `admin123`
- Unidades escolares de exemplo
- Disciplinas básicas
- Turmas de exemplo

### 7. Criar Superusuário (Opcional)

Se preferir criar seu próprio superusuário:

```bash
python manage.py createsuperuser
```

## 🚀 Executando o Projeto

### 1. Iniciar o Servidor de Desenvolvimento

```bash
# Iniciar servidor na porta padrão (8000)
python manage.py runserver

# Ou especificar uma porta
python manage.py runserver 8080

# Ou permitir acesso externo
python manage.py runserver 0.0.0.0:8000
```

### 2. Acessar o Sistema

- **Admin Django:** http://localhost:8000/admin/
- **API Base:** http://localhost:8000/api/
- **Documentação da API:** Consulte o arquivo `API_DOCUMENTATION.md`

### 3. Credenciais de Acesso

**Usuário Administrador (criado automaticamente):**
- Username: `admin`
- Password: `admin123`

## 📁 Estrutura do Projeto

```
escola/
├── apps/                    # Aplicações Django
│   ├── accounts/           # Autenticação e perfis
│   ├── alunos/             # Gestão de alunos
│   ├── professores/        # Gestão de professores
│   ├── administracao/      # Gestão administrativa
│   ├── relatorios/         # Relatórios e estatísticas
│   └── core/               # Utilitários e configurações
├── escola/                 # Configurações do projeto
├── static/                 # Arquivos estáticos
├── media/                  # Arquivos de mídia
├── templates/              # Templates HTML
├── management/             # Comandos personalizados
├── requirements.txt        # Dependências
├── env.example            # Exemplo de variáveis de ambiente
├── README.md              # Documentação principal
├── API_DOCUMENTATION.md   # Documentação da API
└── INSTALACAO.md          # Este arquivo
```

## 🔧 Configurações Adicionais

### Configurar PostgreSQL (Produção)

1. **Instalar PostgreSQL:**
   - [Download PostgreSQL](https://www.postgresql.org/download/)

2. **Criar Banco de Dados:**
```sql
CREATE DATABASE escola_db;
CREATE USER escola_user WITH PASSWORD 'sua-senha';
GRANT ALL PRIVILEGES ON DATABASE escola_db TO escola_user;
```

3. **Atualizar .env:**
```env
DB_NAME=escola_db
DB_USER=escola_user
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432
```

4. **Aplicar Migrações:**
```bash
python manage.py migrate
```

### Configurar Email (Opcional)

Para funcionalidades de email, configure no `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

## 🧪 Testando o Sistema

### 1. Testar API de Autenticação

```bash
# Registrar um novo usuário
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "password": "senha123",
    "first_name": "Usuário",
    "last_name": "Teste",
    "email": "teste@email.com",
    "tipo_usuario": "aluno",
    "unidade_escolar": 1
  }'

# Fazer login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "password": "senha123"
  }'
```

### 2. Testar Endpoints Protegidos

```bash
# Usar o token retornado no login
curl -X GET http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🐛 Solução de Problemas

### Erro: "No module named 'django'"
```bash
# Ativar ambiente virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Database is locked" (SQLite)
```bash
# Parar o servidor e tentar novamente
# Ou usar PostgreSQL em produção
```

### Erro: "Port already in use"
```bash
# Usar uma porta diferente
python manage.py runserver 8080
```

### Erro: "Migration issues"
```bash
# Resetar migrações (CUIDADO: perde dados)
python manage.py migrate --fake-initial
# ou
python manage.py migrate --fake
```

## 📚 Recursos Adicionais

- **Documentação da API:** `API_DOCUMENTATION.md`
- **Configuração do Banco:** `db_config.md`
- **Documentação Principal:** `README.md`

## 🤝 Suporte

Se encontrar problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme se o ambiente virtual está ativo
3. Verifique as configurações no arquivo `.env`
4. Consulte os logs do Django para erros específicos

## 🎉 Próximos Passos

Após a instalação bem-sucedida:

1. Explore a interface administrativa em `/admin/`
2. Teste os endpoints da API
3. Configure usuários e dados de teste
4. Personalize as configurações conforme necessário
5. Implemente funcionalidades específicas do seu projeto

---

**Boa sorte com seu Sistema de Gestão Escolar! 🎓**
