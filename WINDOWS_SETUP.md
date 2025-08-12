# 🪟 Guia de Instalação no Windows - Sistema de Gestão Escolar

Este guia é específico para usuários Windows que querem instalar e executar o Sistema de Gestão Escolar.

## 📋 Pré-requisitos para Windows

### 1. Python
- **Python 3.8+** - [Download Python para Windows](https://www.python.org/downloads/windows/)
- **pip** (vem com Python)
- **Git** - [Download Git para Windows](https://git-scm.com/download/win)

### 2. Verificar Instalações
Abra o **PowerShell** ou **Prompt de Comando** e execute:

```powershell
# Verificar Python
python --version
# ou
py --version

# Verificar pip
pip --version

# Verificar Git
git --version
```

## 🛠️ Instalação no Windows

### 1. Abrir Terminal
- Pressione `Win + R`
- Digite `powershell` e pressione Enter
- Ou use o **Git Bash** se preferir

### 2. Navegar para o Diretório
```powershell
# Navegar para onde quer instalar o projeto
cd C:\Users\SeuUsuario\Documents\projetos
# ou
cd C:\Users\SeuUsuario\Desktop
```

### 3. Clone do Repositório
```powershell
# Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd escola
```

### 4. Criar Ambiente Virtual
```powershell
# Criar ambiente virtual
python -m venv venv
# ou
py -m venv venv

# Ativar ambiente virtual (IMPORTANTE!)
venv\Scripts\activate
```

**Nota:** Após ativar, você verá `(venv)` no início da linha de comando.

### 5. Instalar Dependências
```powershell
# Instalar todas as dependências
pip install -r requirements.txt
```

### 6. Configurar Variáveis de Ambiente
```powershell
# Copiar arquivo de exemplo
copy env.example .env

# Editar o arquivo .env
notepad .env
# ou
code .env  # Se tiver VS Code
```

**Conteúdo do arquivo `.env`:**
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
```

### 7. Configurar Banco de Dados
```powershell
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate
```

### 8. Configurar Dados Iniciais
```powershell
# Executar comando para criar dados iniciais
python manage.py setup_initial_data
```

### 9. Executar o Servidor
```powershell
# Iniciar servidor
python manage.py runserver
```

## 🚀 Acessar o Sistema

Após executar o servidor, acesse:

- **Admin Django:** http://localhost:8000/admin/
- **API Base:** http://localhost:8000/api/

**Credenciais:**
- Username: `admin`
- Password: `admin123`

## 🔧 Comandos Úteis no Windows

### Ativar Ambiente Virtual
```powershell
# Sempre que abrir um novo terminal
venv\Scripts\activate
```

### Desativar Ambiente Virtual
```powershell
deactivate
```

### Criar Superusuário
```powershell
python manage.py createsuperuser
```

### Shell Django
```powershell
python manage.py shell
```

### Coletar Arquivos Estáticos
```powershell
python manage.py collectstatic
```

## 🐛 Problemas Comuns no Windows

### Erro: "python não é reconhecido"
```powershell
# Verificar se Python está no PATH
echo $env:PATH

# Ou usar py em vez de python
py --version
py manage.py runserver
```

### Erro: "pip não é reconhecido"
```powershell
# Reinstalar pip
python -m ensurepip --upgrade
```

### Erro: "venv não é reconhecido"
```powershell
# Instalar virtualenv
pip install virtualenv

# Criar ambiente virtual
virtualenv venv
venv\Scripts\activate
```

### Erro: "Porta 8000 já está em uso"
```powershell
# Usar porta diferente
python manage.py runserver 8080

# Ou matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erro: "Permissão negada"
```powershell
# Executar PowerShell como Administrador
# Ou usar Git Bash
```

### Erro: "Database is locked"
```powershell
# Parar o servidor (Ctrl+C)
# Tentar novamente
python manage.py migrate
```

## 🔧 Configurações Avançadas

### Usar Git Bash (Recomendado)
1. Instalar [Git for Windows](https://git-scm.com/download/win)
2. Abrir **Git Bash**
3. Usar comandos Linux-style:
```bash
# Ativar ambiente virtual
source venv/Scripts/activate

# Comandos normais
python manage.py runserver
```

### Usar VS Code
1. Instalar [Visual Studio Code](https://code.visualstudio.com/)
2. Instalar extensão Python
3. Abrir terminal integrado (Ctrl+`)
4. Seguir os mesmos comandos

### Configurar PostgreSQL no Windows
1. Baixar [PostgreSQL para Windows](https://www.postgresql.org/download/windows/)
2. Instalar com pgAdmin
3. Criar banco de dados
4. Configurar `.env` com dados do PostgreSQL

## 📁 Estrutura de Arquivos no Windows

```
C:\Users\SeuUsuario\projetos\escola\
├── apps\                    # Aplicações Django
├── escola\                  # Configurações do projeto
├── venv\                    # Ambiente virtual
├── static\                  # Arquivos estáticos
├── media\                   # Arquivos de mídia
├── requirements.txt         # Dependências
├── .env                     # Variáveis de ambiente
├── manage.py               # Script de gerenciamento
└── README.md               # Documentação
```

## 🎯 Dicas para Windows

### 1. Sempre Ativar o Ambiente Virtual
```powershell
# Adicionar ao perfil do PowerShell
notepad $PROFILE

# Adicionar linha:
Set-Location C:\Users\SeuUsuario\projetos\escola
venv\Scripts\activate
```

### 2. Usar Aliases Úteis
```powershell
# Criar aliases no PowerShell
Set-Alias -Name rs -Value "python manage.py runserver"
Set-Alias -Name mm -Value "python manage.py makemigrations"
Set-Alias -Name m -Value "python manage.py migrate"
```

### 3. Configurar Editor
```powershell
# Usar VS Code como editor padrão
code .

# Ou usar Notepad++
notepad++ .env
```

## 🔍 Verificar Instalação

Execute estes comandos para verificar se tudo está funcionando:

```powershell
# 1. Verificar Python
python --version

# 2. Verificar Django
python -c "import django; print(django.get_version())"

# 3. Verificar ambiente virtual
echo $env:VIRTUAL_ENV

# 4. Testar servidor
python manage.py runserver
```

## 📞 Suporte para Windows

Se encontrar problemas específicos do Windows:

1. **Verificar permissões** - Executar como Administrador
2. **Verificar PATH** - Python e pip no PATH do sistema
3. **Usar Git Bash** - Interface mais amigável
4. **Reinstalar Python** - Marcar "Add to PATH" na instalação

---

**Agora você pode desenvolver no Windows sem problemas! 🚀**
