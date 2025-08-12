from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Requerimento, ConfiguracaoSistema, LogSistema
from .serializers import (
    RequerimentoSerializer, RequerimentoCreateSerializer, RequerimentoUpdateSerializer,
    ConfiguracaoSistemaSerializer, ConfiguracaoSistemaCreateSerializer,
    LogSistemaSerializer, EstatisticasGeraisSerializer, EstatisticasUnidadeSerializer,
    RequerimentoEstatisticasSerializer
)
from apps.core.permissions import IsAdministrador, IsProfessorOrAdmin
from apps.accounts.models import Perfil, UnidadeEscolar
from apps.alunos.models import Aluno, Turma, AlunoTurma, Trabalho, Nota
from apps.professores.models import Professor, Disciplina


class RequerimentoListView(generics.ListCreateAPIView):
    """Lista e cria requerimentos"""
    serializer_class = RequerimentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['professor', 'tipo', 'prioridade', 'status']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_solicitacao', 'prioridade', 'status']
    
    def get_queryset(self):
        queryset = Requerimento.objects.all()
        
        # Filtrar baseado no tipo de usuário
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'professor':
                # Professor vê apenas seus requerimentos
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(professor=professor)
            elif perfil.tipo_usuario == 'administrador':
                # Admin vê requerimentos da sua unidade
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        professor__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Professor.DoesNotExist):
            pass
            
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RequerimentoCreateSerializer
        return RequerimentoSerializer
    
    def perform_create(self, serializer):
        # Associar automaticamente o professor logado
        try:
            professor = Professor.objects.get(usuario=self.request.user)
            serializer.save(professor=professor)
        except Professor.DoesNotExist:
            raise serializers.ValidationError("Usuário não é um professor")


class RequerimentoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove requerimento"""
    serializer_class = RequerimentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Requerimento.objects.all()
        
        # Filtrar baseado no tipo de usuário
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'professor':
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(professor=professor)
            elif perfil.tipo_usuario == 'administrador':
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        professor__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Professor.DoesNotExist):
            pass
            
        return queryset
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RequerimentoUpdateSerializer
        return RequerimentoSerializer
    
    def perform_update(self, serializer):
        # Se for admin, registrar quem respondeu
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'administrador':
                serializer.save(
                    administrador_resposta=self.request.user,
                    data_resposta=timezone.now()
                )
            else:
                serializer.save()
        except Perfil.DoesNotExist:
            serializer.save()


class ConfiguracaoSistemaListView(generics.ListCreateAPIView):
    """Lista e cria configurações do sistema"""
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for superuser
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ConfiguracaoSistemaCreateSerializer
        return ConfiguracaoSistemaSerializer


class ConfiguracaoSistemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove configuração do sistema"""
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for superuser
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


class LogSistemaListView(generics.ListAPIView):
    """Lista logs do sistema"""
    queryset = LogSistema.objects.all()
    serializer_class = LogSistemaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['usuario', 'tipo', 'ip_address']
    search_fields = ['acao', 'detalhes']
    ordering_fields = ['created_at', 'usuario__username', 'tipo']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for superuser
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    # Filtrar logs de usuários da mesma unidade
                    usuarios_unidade = User.objects.filter(
                        perfil__unidade_escolar=perfil.unidade_escolar
                    )
                    queryset = queryset.filter(usuario__in=usuarios_unidade)
            except Perfil.DoesNotExist:
                pass
        return queryset


# Views para estatísticas e relatórios
class EstatisticasGeraisView(APIView):
    """Estatísticas gerais do sistema"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    
    def get(self, request):
        # Filtrar por unidade escolar se o usuário não for superuser
        unidade_filter = {}
        if not request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.unidade_escolar:
                    unidade_filter = {'unidade_escolar': perfil.unidade_escolar}
            except Perfil.DoesNotExist:
                pass
        
        # Estatísticas
        total_alunos = Aluno.objects.filter(**unidade_filter).count()
        total_professores = Professor.objects.filter(**unidade_filter).count()
        total_turmas = Turma.objects.filter(**unidade_filter).count()
        total_disciplinas = Disciplina.objects.count()  # Disciplinas são globais
        total_requerimentos_pendentes = Requerimento.objects.filter(
            status='pendente'
        ).count()
        total_trabalhos_ativos = Trabalho.objects.filter(ativo=True).count()
        
        data = {
            'total_alunos': total_alunos,
            'total_professores': total_professores,
            'total_turmas': total_turmas,
            'total_disciplinas': total_disciplinas,
            'total_requerimentos_pendentes': total_requerimentos_pendentes,
            'total_trabalhos_ativos': total_trabalhos_ativos,
        }
        
        serializer = EstatisticasGeraisSerializer(data)
        return Response(serializer.data)


class EstatisticasUnidadeView(APIView):
    """Estatísticas de uma unidade específica"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    
    def get(self, request, unidade_id):
        try:
            unidade = UnidadeEscolar.objects.get(id=unidade_id)
            
            # Verificar se o usuário tem acesso a esta unidade
            if not request.user.is_superuser:
                try:
                    perfil = Perfil.objects.get(usuario=request.user)
                    if perfil.unidade_escolar != unidade:
                        return Response(
                            {'error': 'Acesso negado'}, 
                            status=status.HTTP_403_FORBIDDEN
                        )
                except Perfil.DoesNotExist:
                    return Response(
                        {'error': 'Acesso negado'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            # Estatísticas da unidade
            total_alunos = Aluno.objects.filter(unidade_escolar=unidade).count()
            total_professores = Professor.objects.filter(unidade_escolar=unidade).count()
            total_turmas = Turma.objects.filter(unidade_escolar=unidade).count()
            
            # Média das notas da unidade
            notas = Nota.objects.filter(
                turma_disciplina__turma__unidade_escolar=unidade
            )
            media_notas = notas.aggregate(media=Avg('valor'))['media'] or 0.0
            
            # Requerimentos pendentes da unidade
            requerimentos_pendentes = Requerimento.objects.filter(
                professor__unidade_escolar=unidade,
                status='pendente'
            ).count()
            
            data = {
                'unidade': {
                    'id': unidade.id,
                    'nome': unidade.nome,
                    'endereco': unidade.endereco,
                    'telefone': unidade.telefone,
                    'email': unidade.email,
                },
                'total_alunos': total_alunos,
                'total_professores': total_professores,
                'total_turmas': total_turmas,
                'media_notas': round(media_notas, 2),
                'requerimentos_pendentes': requerimentos_pendentes,
            }
            
            serializer = EstatisticasUnidadeSerializer(data)
            return Response(serializer.data)
            
        except UnidadeEscolar.DoesNotExist:
            return Response(
                {'error': 'Unidade escolar não encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class RequerimentoEstatisticasView(APIView):
    """Estatísticas de requerimentos"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    
    def get(self, request):
        # Filtrar por unidade escolar se o usuário não for superuser
        unidade_filter = {}
        if not request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.unidade_escolar:
                    unidade_filter = {'professor__unidade_escolar': perfil.unidade_escolar}
            except Perfil.DoesNotExist:
                pass
        
        # Estatísticas gerais
        total_requerimentos = Requerimento.objects.filter(**unidade_filter).count()
        requerimentos_pendentes = Requerimento.objects.filter(
            **unidade_filter, status='pendente'
        ).count()
        requerimentos_aprovados = Requerimento.objects.filter(
            **unidade_filter, status='aprovado'
        ).count()
        requerimentos_rejeitados = Requerimento.objects.filter(
            **unidade_filter, status='rejeitado'
        ).count()
        
        # Requerimentos por tipo
        requerimentos_por_tipo = Requerimento.objects.filter(
            **unidade_filter
        ).values('tipo').annotate(
            count=Count('id')
        )
        
        # Requerimentos por prioridade
        requerimentos_por_prioridade = Requerimento.objects.filter(
            **unidade_filter
        ).values('prioridade').annotate(
            count=Count('id')
        )
        
        data = {
            'total_requerimentos': total_requerimentos,
            'requerimentos_pendentes': requerimentos_pendentes,
            'requerimentos_aprovados': requerimentos_aprovados,
            'requerimentos_rejeitados': requerimentos_rejeitados,
            'requerimentos_por_tipo': {
                item['tipo']: item['count'] for item in requerimentos_por_tipo
            },
            'requerimentos_por_prioridade': {
                item['prioridade']: item['count'] for item in requerimentos_por_prioridade
            },
        }
        
        serializer = RequerimentoEstatisticasSerializer(data)
        return Response(serializer.data)


# Views para criação de logs
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def criar_log(request):
    """Cria um log do sistema"""
    try:
        tipo = request.data.get('tipo')
        acao = request.data.get('acao')
        detalhes = request.data.get('detalhes', '')
        
        if not tipo or not acao:
            return Response(
                {'error': 'Tipo e ação são obrigatórios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        log = LogSistema.objects.create(
            usuario=request.user,
            tipo=tipo,
            acao=acao,
            detalhes=detalhes,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        serializer = LogSistemaSerializer(log)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
