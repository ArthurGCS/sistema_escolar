# 📚 Documentação da API - Sistema de Gestão Escolar

## 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Tokens)** para autenticação.

### Endpoints de Autenticação

#### 1. Registro de Usuário
```http
POST /api/accounts/register/
```

**Body:**
```json
{
    "username": "joao.silva",
    "password": "senha123",
    "first_name": "João",
    "last_name": "Silva",
    "email": "joao@email.com",
    "tipo_usuario": "aluno",
    "unidade_escolar": 1
}
```

#### 2. Login
```http
POST /api/accounts/login/
```

**Body:**
```json
{
    "username": "joao.silva",
    "password": "senha123"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "joao.silva",
        "first_name": "João",
        "last_name": "Silva",
        "email": "joao@email.com"
    }
}
```

#### 3. Renovar Token
```http
POST /api/accounts/token/refresh/
```

**Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 4. Logout
```http
POST /api/accounts/logout/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

## 🏫 Unidades Escolares

### Listar Unidades Ativas
```http
GET /api/accounts/unidades/
```

### Detalhes da Unidade
```http
GET /api/accounts/unidades/{id}/
```

## 👤 Perfil do Usuário

### Ver Perfil
```http
GET /api/accounts/profile/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

### Atualizar Perfil
```http
PUT /api/accounts/profile/
```

### Alterar Senha
```http
POST /api/accounts/change-password/
```

**Body:**
```json
{
    "old_password": "senha123",
    "new_password": "nova_senha456"
}
```

## 👨‍🎓 Alunos

### Listar Alunos
```http
GET /api/alunos/
```

**Filtros disponíveis:**
- `unidade_escolar`: ID da unidade
- `status`: ativo, inativo, transferido, concluido
- `sexo`: M, F
- `search`: Busca por nome ou matrícula

### Criar Aluno
```http
POST /api/alunos/
```

**Body:**
```json
{
    "username": "maria.santos",
    "password": "senha123",
    "first_name": "Maria",
    "last_name": "Santos",
    "email": "maria@email.com",
    "matricula": "2024001",
    "unidade_escolar": 1,
    "data_nascimento": "2010-05-15",
    "sexo": "F",
    "endereco": "Rua das Flores, 123",
    "nome_responsavel": "João Santos",
    "telefone_responsavel": "(11) 99999-9999",
    "email_responsavel": "joao@email.com"
}
```

### Detalhes do Aluno
```http
GET /api/alunos/{id}/
```

### Atualizar Aluno
```http
PUT /api/alunos/{id}/
```

### Remover Aluno
```http
DELETE /api/alunos/{id}/
```

## 🏫 Turmas

### Listar Turmas
```http
GET /api/alunos/turmas/
```

**Filtros disponíveis:**
- `unidade_escolar`: ID da unidade
- `ano`: Ano letivo
- `turno`: manha, tarde, noite, integral
- `ativa`: true/false

### Criar Turma
```http
POST /api/alunos/turmas/
```

**Body:**
```json
{
    "nome": "1º Ano A",
    "unidade_escolar": 1,
    "ano": 2024,
    "turno": "manha",
    "ativa": true
}
```

### Detalhes da Turma
```http
GET /api/alunos/turmas/{id}/
```

## 📚 Trabalhos

### Listar Trabalhos (Alunos)
```http
GET /api/alunos/trabalhos/
```

**Filtros disponíveis:**
- `turma_disciplina__turma`: ID da turma
- `turma_disciplina__disciplina`: ID da disciplina
- `tipo`: individual, grupo, projeto, pesquisa
- `ativo`: true/false

### Detalhes do Trabalho
```http
GET /api/alunos/trabalhos/{id}/
```

### Meus Trabalhos (Aluno logado)
```http
GET /api/alunos/meus-trabalhos/
```

## 📤 Entregas de Trabalhos

### Listar Entregas
```http
GET /api/alunos/entregas/
```

### Criar Entrega (Aluno)
```http
POST /api/alunos/entregas/
```

**Body (multipart/form-data):**
```json
{
    "trabalho": 1,
    "arquivo": <file>,
    "observacoes": "Observações sobre a entrega"
}
```

### Detalhes da Entrega
```http
GET /api/alunos/entregas/{id}/
```

## 📊 Notas

### Listar Notas (Professores/Admin)
```http
GET /api/alunos/notas/
```

### Criar Nota (Professor)
```http
POST /api/alunos/notas/
```

**Body:**
```json
{
    "aluno": 1,
    "turma_disciplina": 1,
    "tipo": "prova1",
    "valor": 8.5,
    "data_avaliacao": "2024-08-15",
    "observacoes": "Bom desempenho"
}
```

### Minhas Notas (Aluno logado)
```http
GET /api/alunos/minhas-notas/
```

## 👨‍🏫 Professores

### Listar Professores (Admin)
```http
GET /api/professores/
```

### Criar Professor (Admin)
```http
POST /api/professores/
```

**Body:**
```json
{
    "username": "prof.maria",
    "password": "senha123",
    "first_name": "Maria",
    "last_name": "Silva",
    "email": "maria@escola.com",
    "matricula": "PROF001",
    "unidade_escolar": 1,
    "data_nascimento": "1985-03-20",
    "sexo": "F",
    "endereco": "Av. Principal, 456",
    "telefone": "(11) 88888-8888",
    "email": "maria@escola.com",
    "formacao": "Licenciatura em Matemática"
}
```

### Detalhes do Professor
```http
GET /api/professores/{id}/
```

## 📖 Disciplinas

### Listar Disciplinas
```http
GET /api/professores/disciplinas/
```

### Criar Disciplina
```http
POST /api/professores/disciplinas/
```

**Body:**
```json
{
    "nome": "Matemática",
    "codigo": "MAT001",
    "descricao": "Matemática do Ensino Fundamental",
    "carga_horaria": 80,
    "ativa": true
}
```

### Detalhes da Disciplina
```http
GET /api/professores/disciplinas/{id}/
```

## 📊 Estatísticas do Professor

### Estatísticas Gerais
```http
GET /api/professores/estatisticas/
```

### Minhas Disciplinas
```http
GET /api/professores/minhas-disciplinas/
```

### Estatísticas da Disciplina
```http
GET /api/professores/disciplinas/{id}/estatisticas/
```

## 📝 Trabalhos do Professor

### Listar/Criar Trabalhos
```http
GET /api/professores/trabalhos/
POST /api/professores/trabalhos/
```

### Listar/Criar Notas
```http
GET /api/professores/notas/
POST /api/professores/notas/
```

## 🏢 Administração

### Requerimentos

#### Listar Requerimentos
```http
GET /api/administracao/requerimentos/
```

#### Criar Requerimento (Professor)
```http
POST /api/administracao/requerimentos/
```

**Body:**
```json
{
    "titulo": "Solicitação de Material",
    "descricao": "Preciso de novos livros para a turma",
    "tipo": "material",
    "prioridade": "media"
}
```

#### Atualizar Requerimento (Admin)
```http
PUT /api/administracao/requerimentos/{id}/
```

**Body:**
```json
{
    "status": "aprovado",
    "resposta": "Material será entregue na próxima semana"
}
```

### Configurações do Sistema

#### Listar Configurações
```http
GET /api/administracao/configuracoes/
```

#### Criar Configuração
```http
POST /api/administracao/configuracoes/
```

**Body:**
```json
{
    "unidade_escolar": 1,
    "ano_letivo_atual": 2024,
    "periodo_inscricao_aberto": true,
    "data_inicio_ano_letivo": "2024-02-01",
    "data_fim_ano_letivo": "2024-12-15",
    "max_alunos_por_turma": 40,
    "nota_minima_aprovacao": 6.0
}
```

### Logs do Sistema

#### Listar Logs
```http
GET /api/administracao/logs/
```

#### Criar Log
```http
POST /api/administracao/logs/criar/
```

**Body:**
```json
{
    "tipo": "login",
    "acao": "Usuário fez login",
    "detalhes": "Login realizado com sucesso"
}
```

### Estatísticas e Relatórios

#### Estatísticas Gerais
```http
GET /api/administracao/estatisticas-gerais/
```

#### Estatísticas da Unidade
```http
GET /api/administracao/estatisticas-unidade/{id}/
```

#### Estatísticas de Requerimentos
```http
GET /api/administracao/estatisticas-requerimentos/
```

## 🔐 Permissões

### Tipos de Usuário

1. **Aluno**: Pode ver suas notas, trabalhos e fazer entregas
2. **Professor**: Pode gerenciar suas disciplinas, criar trabalhos e notas
3. **Administrador**: Acesso completo ao sistema da sua unidade
4. **Superuser**: Acesso completo a todo o sistema

### Headers Necessários

Para todas as requisições autenticadas, inclua:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## 📋 Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Não autenticado
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## 🔍 Filtros e Ordenação

A maioria dos endpoints suporta:

### Filtros
Use parâmetros de query: `?campo=valor`

### Busca
Use parâmetro `search`: `?search=termo`

### Ordenação
Use parâmetro `ordering`: `?ordering=campo` ou `?ordering=-campo` (decrescente)

### Paginação
Use parâmetros `page` e `page_size`: `?page=1&page_size=20`

## 📝 Exemplos de Uso

### Exemplo 1: Login e Acesso ao Perfil
```bash
# 1. Fazer login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 2. Usar o token para acessar o perfil
curl -X GET http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Bearer <access_token>"
```

### Exemplo 2: Criar um Aluno
```bash
curl -X POST http://localhost:8000/api/alunos/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao.aluno",
    "password": "senha123",
    "first_name": "João",
    "last_name": "Aluno",
    "email": "joao@email.com",
    "matricula": "2024001",
    "unidade_escolar": 1,
    "data_nascimento": "2010-05-15",
    "sexo": "M",
    "endereco": "Rua das Flores, 123",
    "nome_responsavel": "Maria Aluno",
    "telefone_responsavel": "(11) 99999-9999",
    "email_responsavel": "maria@email.com"
  }'
```

### Exemplo 3: Listar Trabalhos com Filtros
```bash
curl -X GET "http://localhost:8000/api/alunos/trabalhos/?tipo=individual&ativo=true&ordering=-data_entrega" \
  -H "Authorization: Bearer <access_token>"
```

## 🚀 Próximos Passos

1. **Frontend**: Implementar interface web com Django Templates
2. **Relatórios**: Adicionar geração de relatórios em PDF
3. **Notificações**: Implementar sistema de notificações
4. **Testes**: Adicionar testes automatizados
5. **Deploy**: Configurar para produção com PostgreSQL

---

**Desenvolvido com ❤️ usando Django REST Framework**
