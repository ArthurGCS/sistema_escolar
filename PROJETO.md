# 🎓 Sistema de Gestão Escolar - Visão Geral

## 📋 Sobre o Projeto

O **Sistema de Gestão Escolar** é uma aplicação web desenvolvida em Django que oferece uma solução completa para gerenciamento de instituições educacionais. O sistema suporta múltiplas unidades escolares e implementa controle de acesso baseado em roles (RBAC) para três tipos de usuários: Alunos, Professores e Administração.

## 🎯 Objetivos

- **Centralizar** a gestão de dados escolares
- **Automatizar** processos administrativos
- **Facilitar** o acompanhamento acadêmico
- **Melhorar** a comunicação entre alunos, professores e administração
- **Gerar** relatórios e estatísticas educacionais

## 👥 Público-Alvo

- **Escolas Municipais e Estaduais**
- **Colégios Particulares**
- **Instituições de Ensino Fundamental e Médio**
- **Secretarias de Educação**

## 🏗️ Arquitetura

### Backend
- **Django 4.2+** - Framework web principal
- **Django REST Framework** - API REST
- **SimpleJWT** - Autenticação via tokens
- **PostgreSQL/SQLite** - Banco de dados

### Frontend (MVP)
- **Django Templates** - Interface web
- **Bootstrap** - Framework CSS
- **JavaScript** - Interatividade

### Futuro
- **Next.js/React** - Frontend moderno
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização

## 🔐 Sistema de Autenticação

### JWT (JSON Web Tokens)
- **Access Token** - 1 hora de validade
- **Refresh Token** - 1 dia de validade
- **Autenticação Bearer** - Headers HTTP

### Controle de Acesso (RBAC)
- **Aluno** - Visualizar notas, enviar trabalhos
- **Professor** - Gerenciar turmas, lançar notas
- **Administração** - Gestão completa do sistema

## 📊 Funcionalidades por Perfil

### 👨‍🎓 Aluno
- **Visualizar notas** por disciplina
- **Enviar trabalhos** acadêmicos
- **Acompanhar frequência**
- **Ver calendário escolar**

### 👨‍🏫 Professor
- **Gerenciar turmas** e disciplinas
- **Lançar notas** e frequência
- **Criar e corrigir trabalhos**
- **Gerar relatórios** de turma
- **Solicitar recursos** à administração

### 👨‍💼 Administração
- **Criar e gerenciar turmas**
- **Matricular alunos**
- **Cadastrar professores**
- **Configurar disciplinas**
- **Gerar relatórios** institucionais
- **Gerenciar unidades escolares**

## 🗄️ Modelos de Dados

### Core
- **UnidadeEscolar** - Instituições
- **Perfil** - Dados dos usuários
- **User** - Autenticação Django

### Alunos
- **Aluno** - Dados do estudante
- **Turma** - Classes escolares
- **AlunoTurma** - Relacionamento aluno-turma
- **Trabalho** - Atividades acadêmicas
- **EntregaTrabalho** - Submissões dos alunos
- **Nota** - Avaliações

### Professores
- **Professor** - Dados do docente
- **Disciplina** - Matérias escolares
- **ProfessorDisciplina** - Relacionamento professor-disciplina
- **TurmaDisciplina** - Relacionamento turma-disciplina

### Administração
- **Requerimento** - Solicitações dos professores
- **ConfiguracaoSistema** - Configurações gerais
- **LogSistema** - Registro de atividades

## 🔌 API REST

### Endpoints Principais
- **`/api/accounts/`** - Autenticação e perfis
- **`/api/alunos/`** - Gestão de alunos
- **`/api/professores/`** - Gestão de professores
- **`/api/administracao/`** - Gestão administrativa
- **`/api/relatorios/`** - Relatórios e estatísticas

### Recursos da API
- **Filtros** por múltiplos critérios
- **Busca** textual
- **Ordenação** personalizada
- **Paginação** automática
- **Validação** de dados
- **Documentação** completa

## 📈 Relatórios e Estatísticas

### Para Professores
- **Desempenho** por turma
- **Médias** por disciplina
- **Frequência** dos alunos
- **Progresso** acadêmico

### Para Administração
- **Estatísticas gerais** da instituição
- **Relatórios** por unidade escolar
- **Análise** de requerimentos
- **Métricas** de performance

## 🚀 Roadmap

### Fase 1 - MVP ✅
- [x] Estrutura base do projeto
- [x] Sistema de autenticação
- [x] API REST completa
- [x] Modelos de dados
- [x] Controle de acesso

### Fase 2 - Frontend
- [ ] Templates Django
- [ ] Interface responsiva
- [ ] Dashboard interativo
- [ ] Formulários dinâmicos

### Fase 3 - Funcionalidades Avançadas
- [ ] Sistema de notificações
- [ ] Upload de arquivos
- [ ] Relatórios em PDF
- [ ] Exportação de dados

### Fase 4 - Modernização
- [ ] Frontend em React/Next.js
- [ ] PWA (Progressive Web App)
- [ ] Mobile app
- [ ] Integração com sistemas externos

## 🔧 Configuração Técnica

### Desenvolvimento
- **SQLite** - Banco de dados local
- **DEBUG=True** - Modo desenvolvimento
- **Hot reload** - Recarregamento automático

### Produção
- **PostgreSQL** - Banco de dados robusto
- **Gunicorn** - Servidor WSGI
- **Nginx** - Proxy reverso
- **Redis** - Cache e sessões

## 📚 Documentação

- **`INSTALACAO.md`** - Guia completo de instalação
- **`QUICK_START.md`** - Setup rápido
- **`API_DOCUMENTATION.md`** - Documentação da API
- **`db_config.md`** - Configuração do banco

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Desenvolva** e teste suas mudanças
4. **Submeta** um pull request

### Padrões de Código
- **PEP 8** - Estilo Python
- **Docstrings** - Documentação de funções
- **Type hints** - Tipagem (quando possível)
- **Testes** - Cobertura mínima de 80%

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

- **Issues** - GitHub Issues
- **Documentação** - Arquivos .md
- **Email** - [seu-email@exemplo.com]

---

**Desenvolvido com ❤️ para melhorar a educação brasileira**
