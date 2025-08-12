# Configuração do Banco de Dados

## SQLite (Desenvolvimento)

Para desenvolvimento, o sistema usa SQLite por padrão. Não é necessária configuração adicional.

## PostgreSQL (Produção)

### 1. Instalar PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql postgresql-server postgresql-contrib
```

**Windows:**
Baixe e instale do site oficial: https://www.postgresql.org/download/windows/

### 2. Criar Banco de Dados

```bash
# Conectar como usuário postgres
sudo -u postgres psql

# Criar usuário e banco
CREATE USER escola_user WITH PASSWORD 'sua_senha_aqui';
CREATE DATABASE escola_db OWNER escola_user;
GRANT ALL PRIVILEGES ON DATABASE escola_db TO escola_user;
\q
```

### 3. Configurar Variáveis de Ambiente

Edite o arquivo `.env`:

```env
# Configurações do Banco de Dados
DB_NAME=escola_db
DB_USER=escola_user
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=5432
```

### 4. Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Configurar Dados Iniciais

```bash
python manage.py setup_initial_data
```

## Backup e Restore

### Backup
```bash
pg_dump -U escola_user -h localhost escola_db > backup_escola.sql
```

### Restore
```bash
psql -U escola_user -h localhost escola_db < backup_escola.sql
```

## Configurações de Performance

### PostgreSQL (postgresql.conf)
```conf
# Configurações recomendadas para produção
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
```

### Índices Recomendados
```sql
-- Índices para melhorar performance
CREATE INDEX idx_aluno_matricula ON apps_aluno(matricula);
CREATE INDEX idx_professor_matricula ON apps_professor(matricula);
CREATE INDEX idx_nota_aluno ON apps_nota(aluno_id);
CREATE INDEX idx_nota_turma_disciplina ON apps_nota(turma_disciplina_id);
CREATE INDEX idx_trabalho_turma_disciplina ON apps_trabalho(turma_disciplina_id);
```
