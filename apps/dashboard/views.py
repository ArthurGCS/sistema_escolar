from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from apps.accounts.models import Perfil
from apps.alunos.models import Aluno, Turma
from apps.professores.models import Professor, Disciplina
from apps.administracao.models import Requerimento


@login_required
def home(request):
    """Dashboard principal"""
    try:
        perfil = Perfil.objects.get(usuario=request.user)
    except Perfil.DoesNotExist:
        perfil = None
    
    # Estatísticas gerais
    context = {
        'perfil': perfil,
        'total_alunos': Aluno.objects.count(),
        'total_professores': Professor.objects.count(),
        'total_turmas': Turma.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
    }
    
    # Estatísticas por unidade escolar
    if perfil and perfil.unidade_escolar:
        context.update({
            'alunos_unidade': Aluno.objects.filter(unidade_escolar=perfil.unidade_escolar).count(),
            'professores_unidade': Professor.objects.filter(unidade_escolar=perfil.unidade_escolar).count(),
            'turmas_unidade': Turma.objects.filter(unidade_escolar=perfil.unidade_escolar).count(),
        })
    
    # Estatísticas específicas por tipo de usuário
    if perfil:
        if perfil.tipo_usuario == 'aluno':
            context.update(get_aluno_stats(request.user))
        elif perfil.tipo_usuario == 'professor':
            context.update(get_professor_stats(request.user))
        elif perfil.tipo_usuario == 'administrador':
            context.update(get_admin_stats(request.user))
    
    return render(request, 'dashboard/home.html', context)


def get_aluno_stats(user):
    """Estatísticas específicas para alunos"""
    try:
        from apps.alunos.models import Aluno, Nota
        aluno = Aluno.objects.get(usuario=user)
        
        # Notas do aluno
        notas = Nota.objects.filter(aluno=aluno)
        media_geral = notas.aggregate(media=Avg('valor'))['media'] or 0
        
        # Trabalhos do aluno
        from apps.alunos.models import EntregaTrabalho
        trabalhos_entregues = EntregaTrabalho.objects.filter(aluno=aluno).count()
        
        return {
            'media_geral': round(media_geral, 2),
            'total_notas': notas.count(),
            'trabalhos_entregues': trabalhos_entregues,
            'aluno': aluno,
        }
    except Aluno.DoesNotExist:
        return {}


def get_professor_stats(user):
    """Estatísticas específicas para professores"""
    try:
        from apps.professores.models import Professor, TurmaDisciplina
        professor = Professor.objects.get(usuario=user)
        
        # Disciplinas do professor
        turmas_disciplinas = TurmaDisciplina.objects.filter(professor=professor)
        total_disciplinas = turmas_disciplinas.count()
        
        # Trabalhos do professor
        from apps.alunos.models import Trabalho
        trabalhos = Trabalho.objects.filter(turma_disciplina__professor=professor)
        total_trabalhos = trabalhos.count()
        
        # Requerimentos do professor
        requerimentos = Requerimento.objects.filter(professor=professor)
        requerimentos_pendentes = requerimentos.filter(status='pendente').count()
        
        return {
            'total_disciplinas_professor': total_disciplinas,
            'total_trabalhos': total_trabalhos,
            'requerimentos_pendentes': requerimentos_pendentes,
            'professor': professor,
        }
    except Professor.DoesNotExist:
        return {}


def get_admin_stats(user):
    """Estatísticas específicas para administradores"""
    try:
        perfil = Perfil.objects.get(usuario=user)
        
        # Requerimentos pendentes
        requerimentos_pendentes = Requerimento.objects.filter(status='pendente')
        if perfil.unidade_escolar:
            requerimentos_pendentes = requerimentos_pendentes.filter(
                professor__unidade_escolar=perfil.unidade_escolar
            )
        
        # Estatísticas por status
        requerimentos_por_status = Requerimento.objects.values('status').annotate(
            total=Count('id')
        )
        
        return {
            'requerimentos_pendentes': requerimentos_pendentes.count(),
            'requerimentos_por_status': requerimentos_por_status,
        }
    except Perfil.DoesNotExist:
        return {}


@login_required
def about(request):
    """Página sobre o sistema"""
    return render(request, 'dashboard/about.html')


@login_required
def help_page(request):
    """Página de ajuda"""
    return render(request, 'dashboard/help.html')
