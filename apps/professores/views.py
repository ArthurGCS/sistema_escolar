from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User

from .models import Professor, Disciplina, ProfessorDisciplina, TurmaDisciplina
from .serializers import (
    ProfessorSerializer, ProfessorCreateSerializer, DisciplinaSerializer,
    ProfessorDisciplinaSerializer, ProfessorDisciplinaCreateSerializer,
    TurmaDisciplinaSerializer, TurmaDisciplinaCreateSerializer,
    ProfessorEstatisticasSerializer, DisciplinaEstatisticasSerializer
)
from apps.core.permissions import IsProfessor, IsAdministrador, IsProfessorOrAdmin
from apps.accounts.models import Perfil
from apps.alunos.models import Aluno, AlunoTurma, Trabalho, Nota


class ProfessorListView(generics.ListCreateAPIView):
    """Lista e cria professores"""
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unidade_escolar', 'status', 'sexo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'matricula']
    ordering_fields = ['usuario__first_name', 'matricula', 'data_nascimento']
    
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
            return ProfessorCreateSerializer
        return ProfessorSerializer


class ProfessorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove professor"""
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
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


class DisciplinaListView(generics.ListCreateAPIView):
    """Lista e cria disciplinas"""
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativa']
    search_fields = ['nome', 'codigo']
    ordering_fields = ['nome', 'codigo']


class DisciplinaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove disciplina"""
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]


class ProfessorDisciplinaListView(generics.ListCreateAPIView):
    """Lista e cria relacionamentos professor-disciplina"""
    queryset = ProfessorDisciplina.objects.all()
    serializer_class = ProfessorDisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['professor', 'disciplina', 'ativo']
    ordering_fields = ['professor__usuario__first_name', 'disciplina__nome']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for superuser
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(professor__unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProfessorDisciplinaCreateSerializer
        return ProfessorDisciplinaSerializer


class ProfessorDisciplinaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove relacionamento professor-disciplina"""
    queryset = ProfessorDisciplina.objects.all()
    serializer_class = ProfessorDisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for superuser
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(professor__unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


class TurmaDisciplinaListView(generics.ListCreateAPIView):
    """Lista e cria relacionamentos turma-disciplina"""
    queryset = TurmaDisciplina.objects.all()
    serializer_class = TurmaDisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['turma', 'disciplina', 'professor', 'ativo']
    ordering_fields = ['turma__nome', 'disciplina__nome']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for superuser
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(turma__unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TurmaDisciplinaCreateSerializer
        return TurmaDisciplinaSerializer


class TurmaDisciplinaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove relacionamento turma-disciplina"""
    queryset = TurmaDisciplina.objects.all()
    serializer_class = TurmaDisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for superuser
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(turma__unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


# Views específicas para professores
class ProfessorMinhasDisciplinasView(generics.ListAPIView):
    """Lista disciplinas do professor logado"""
    serializer_class = TurmaDisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessor]
    
    def get_queryset(self):
        try:
            professor = Professor.objects.get(usuario=self.request.user)
            return TurmaDisciplina.objects.filter(professor=professor, ativo=True)
        except Professor.DoesNotExist:
            return TurmaDisciplina.objects.none()


class ProfessorEstatisticasView(APIView):
    """Estatísticas do professor logado"""
    permission_classes = [permissions.IsAuthenticated, IsProfessor]
    
    def get(self, request):
        try:
            professor = Professor.objects.get(usuario=request.user)
            
            # Buscar turmas do professor
            turmas_disciplina = TurmaDisciplina.objects.filter(
                professor=professor, ativo=True
            )
            
            # Estatísticas
            total_disciplinas = turmas_disciplina.values('disciplina').distinct().count()
            total_turmas = turmas_disciplina.count()
            
            # Total de alunos
            turmas_ids = turmas_disciplina.values_list('turma_id', flat=True)
            total_alunos = AlunoTurma.objects.filter(
                turma_id__in=turmas_ids, ativo=True
            ).count()
            
            # Trabalhos pendentes (sem nota)
            trabalhos_pendentes = Trabalho.objects.filter(
                turma_disciplina__professor=professor,
                ativo=True
            ).count()
            
            # Notas para lançar (trabalhos sem nota)
            notas_para_lancar = 0  # Será calculado baseado nas entregas sem nota
            
            data = {
                'total_disciplinas': total_disciplinas,
                'total_turmas': total_turmas,
                'total_alunos': total_alunos,
                'trabalhos_pendentes': trabalhos_pendentes,
                'notas_para_lancar': notas_para_lancar,
            }
            
            serializer = ProfessorEstatisticasSerializer(data)
            return Response(serializer.data)
            
        except Professor.DoesNotExist:
            return Response(
                {'error': 'Professor não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class DisciplinaEstatisticasView(APIView):
    """Estatísticas de uma disciplina específica"""
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    
    def get(self, request, disciplina_id):
        try:
            disciplina = Disciplina.objects.get(id=disciplina_id)
            
            # Verificar se o professor tem acesso a esta disciplina
            if not request.user.is_superuser:
                try:
                    perfil = Perfil.objects.get(usuario=request.user)
                    if perfil.tipo_usuario == 'professor':
                        professor = Professor.objects.get(usuario=request.user)
                        if not TurmaDisciplina.objects.filter(
                            professor=professor, disciplina=disciplina
                        ).exists():
                            return Response(
                                {'error': 'Acesso negado'}, 
                                status=status.HTTP_403_FORBIDDEN
                            )
                except (Perfil.DoesNotExist, Professor.DoesNotExist):
                    return Response(
                        {'error': 'Acesso negado'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            # Estatísticas
            turmas_disciplina = TurmaDisciplina.objects.filter(
                disciplina=disciplina, ativo=True
            )
            
            total_turmas = turmas_disciplina.count()
            
            # Total de alunos
            turmas_ids = turmas_disciplina.values_list('turma_id', flat=True)
            total_alunos = AlunoTurma.objects.filter(
                turma_id__in=turmas_ids, ativo=True
            ).count()
            
            # Média das notas
            notas = Nota.objects.filter(
                turma_disciplina__disciplina=disciplina
            )
            media_notas = notas.aggregate(media=Avg('valor'))['media'] or 0.0
            
            # Trabalhos ativos
            trabalhos_ativos = Trabalho.objects.filter(
                turma_disciplina__disciplina=disciplina,
                ativo=True
            ).count()
            
            data = {
                'disciplina': DisciplinaSerializer(disciplina).data,
                'total_turmas': total_turmas,
                'total_alunos': total_alunos,
                'media_notas': round(media_notas, 2),
                'trabalhos_ativos': trabalhos_ativos,
            }
            
            serializer = DisciplinaEstatisticasSerializer(data)
            return Response(serializer.data)
            
        except Disciplina.DoesNotExist:
            return Response(
                {'error': 'Disciplina não encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )


# Views para criação de trabalhos e notas
class ProfessorTrabalhosView(generics.ListCreateAPIView):
    """Lista e cria trabalhos do professor"""
    from apps.alunos.serializers import TrabalhoSerializer, TrabalhoCreateSerializer
    
    serializer_class = TrabalhoSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessor]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['turma_disciplina__turma', 'turma_disciplina__disciplina', 'tipo', 'ativo']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_entrega', 'titulo']
    
    def get_queryset(self):
        try:
            professor = Professor.objects.get(usuario=self.request.user)
            return Trabalho.objects.filter(
                turma_disciplina__professor=professor
            )
        except Professor.DoesNotExist:
            return Trabalho.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrabalhoCreateSerializer
        return TrabalhoSerializer


class ProfessorNotasView(generics.ListCreateAPIView):
    """Lista e cria notas do professor"""
    from apps.alunos.serializers import NotaSerializer, NotaCreateSerializer
    
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessor]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['aluno', 'turma_disciplina', 'tipo']
    ordering_fields = ['data_avaliacao', 'valor']
    
    def get_queryset(self):
        try:
            professor = Professor.objects.get(usuario=self.request.user)
            return Nota.objects.filter(
                turma_disciplina__professor=professor
            )
        except Professor.DoesNotExist:
            return Nota.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotaCreateSerializer
        return NotaSerializer
