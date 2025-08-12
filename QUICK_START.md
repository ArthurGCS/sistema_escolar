# ⚡ Quick Start - Sistema de Gestão Escolar

Guia rápido para desenvolvedores experientes que querem rodar o projeto rapidamente.

## 🚀 Setup Rápido (5 minutos)

```bash
# 1. Clone e entre no projeto
git clone <URL_DO_REPOSITORIO>
cd escola

# 2. Ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Dependências
pip install -r requirements.txt

# 4. Configuração
cp env.example .env

# 5. Banco de dados
python manage.py makemigrations
python manage.py migrate

# 6. Dados iniciais
python manage.py setup_initial_data

# 7. Rodar
python manage.py runserver
```

## 🔑 Acesso Rápido

- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/
- **Login:** `admin` / `admin123`

## 📋 Comandos Úteis

```bash
# Criar superusuário
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic

# Backup do banco
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json
```

## 🔧 Configurações Rápidas

### PostgreSQL
```bash
# Instalar psycopg2
pip install psycopg2-binary

# Configurar .env
DB_NAME=escola_db
DB_USER=escola_user
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432
```

### Email
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

## 🧪 Teste Rápido da API

```bash
# Login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Usar token retornado
curl -X GET http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

## 📁 Estrutura Essencial

```
escola/
├── apps/
│   ├── accounts/     # Auth & Users
│   ├── alunos/       # Students
│   ├── professores/  # Teachers
│   ├── administracao/ # Admin
│   └── core/         # Utils
├── escola/           # Settings
├── requirements.txt
└── manage.py
```

## 🐛 Problemas Comuns

```bash
# Porta ocupada
python manage.py runserver 8080

# Migrações travadas
python manage.py migrate --fake-initial

# Dependências
pip install -r requirements.txt --force-reinstall
```

---

**Pronto! Agora você pode começar a desenvolver! 🎯**
