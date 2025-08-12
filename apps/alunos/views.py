from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Aluno, Turma, AlunoTurma, Trabalho, EntregaTrabalho, Nota
from .serializers import (
    AlunoSerializer, AlunoCreateSerializer, TurmaSerializer, AlunoTurmaSerializer,
    TrabalhoSerializer, EntregaTrabalhoSerializer, EntregaTrabalhoCreateSerializer,
    NotaSerializer, NotaCreateSerializer
)
from apps.core.permissions import IsAluno, IsProfessor, IsAdministrador, IsProfessorOrAdmin
from apps.accounts.models import Perfil


class AlunoListView(generics.ListCreateAPIView):
    """Lista e cria alunos"""
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unidade_escolar', 'status', 'sexo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'matricula']
    ordering_fields = ['usuario__first_name', 'matricula', 'data_nascimento']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for admin
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
            return AlunoCreateSerializer
        return AlunoSerializer


class AlunoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove aluno"""
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for admin
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


class TurmaListView(generics.ListCreateAPIView):
    """Lista e cria turmas"""
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unidade_escolar', 'ano', 'turno', 'ativa']
    search_fields = ['nome']
    ordering_fields = ['nome', 'ano', 'turno']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for admin
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


class TurmaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove turma"""
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for admin
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


class AlunoTurmaListView(generics.ListCreateAPIView):
    """Lista e cria relacionamentos aluno-turma"""
    queryset = AlunoTurma.objects.all()
    serializer_class = AlunoTurmaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['turma', 'aluno', 'ativo']
    ordering_fields = ['data_entrada', 'aluno__usuario__first_name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for admin
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(turma__unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


class AlunoTurmaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove relacionamento aluno-turma"""
    queryset = AlunoTurma.objects.all()
    serializer_class = AlunoTurmaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por unidade escolar se o usuário não for admin
        if not self.request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=self.request.user)
                if perfil.unidade_escolar:
                    queryset = queryset.filter(turma__unidade_escolar=perfil.unidade_escolar)
            except Perfil.DoesNotExist:
                pass
        return queryset


class TrabalhoListView(generics.ListAPIView):
    """Lista trabalhos (alunos veem apenas os da sua turma)"""
    serializer_class = TrabalhoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['turma_disciplina__turma', 'turma_disciplina__disciplina', 'tipo', 'ativo']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_entrega', 'titulo']
    
    def get_queryset(self):
        queryset = Trabalho.objects.filter(ativo=True)
        
        # Se for aluno, mostrar apenas trabalhos da sua turma
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'aluno':
                # Buscar turmas do aluno
                aluno = Aluno.objects.get(usuario=self.request.user)
                turmas_aluno = AlunoTurma.objects.filter(
                    aluno=aluno, ativo=True
                ).values_list('turma_id', flat=True)
                queryset = queryset.filter(
                    turma_disciplina__turma_id__in=turmas_aluno
                )
            elif perfil.tipo_usuario == 'professor':
                # Professor vê trabalhos das suas disciplinas
                from apps.professores.models import Professor
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(
                    turma_disciplina__professor=professor
                )
            elif perfil.tipo_usuario == 'administrador':
                # Admin vê todos os trabalhos da sua unidade
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        turma_disciplina__turma__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Aluno.DoesNotExist):
            pass
            
        return queryset


class TrabalhoDetailView(generics.RetrieveAPIView):
    """Detalhes de trabalho"""
    queryset = Trabalho.objects.filter(ativo=True)
    serializer_class = TrabalhoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Aplicar os mesmos filtros da lista
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'aluno':
                aluno = Aluno.objects.get(usuario=self.request.user)
                turmas_aluno = AlunoTurma.objects.filter(
                    aluno=aluno, ativo=True
                ).values_list('turma_id', flat=True)
                queryset = queryset.filter(
                    turma_disciplina__turma_id__in=turmas_aluno
                )
            elif perfil.tipo_usuario == 'professor':
                from apps.professores.models import Professor
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(
                    turma_disciplina__professor=professor
                )
            elif perfil.tipo_usuario == 'administrador':
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        turma_disciplina__turma__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Aluno.DoesNotExist):
            pass
            
        return queryset


class EntregaTrabalhoListView(generics.ListCreateAPIView):
    """Lista e cria entregas de trabalhos"""
    serializer_class = EntregaTrabalhoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['trabalho', 'aluno', 'trabalho__tipo']
    ordering_fields = ['data_entrega', 'trabalho__titulo']
    
    def get_queryset(self):
        queryset = EntregaTrabalho.objects.all()
        
        # Filtrar baseado no tipo de usuário
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'aluno':
                # Aluno vê apenas suas entregas
                aluno = Aluno.objects.get(usuario=self.request.user)
                queryset = queryset.filter(aluno=aluno)
            elif perfil.tipo_usuario == 'professor':
                # Professor vê entregas dos trabalhos das suas disciplinas
                from apps.professores.models import Professor
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(
                    trabalho__turma_disciplina__professor=professor
                )
            elif perfil.tipo_usuario == 'administrador':
                # Admin vê todas as entregas da sua unidade
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        trabalho__turma_disciplina__turma__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Aluno.DoesNotExist):
            pass
            
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EntregaTrabalhoCreateSerializer
        return EntregaTrabalhoSerializer
    
    def perform_create(self, serializer):
        # Associar automaticamente o aluno logado
        try:
            aluno = Aluno.objects.get(usuario=self.request.user)
            serializer.save(aluno=aluno)
        except Aluno.DoesNotExist:
            raise serializers.ValidationError("Usuário não é um aluno")


class EntregaTrabalhoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove entrega de trabalho"""
    serializer_class = EntregaTrabalhoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = EntregaTrabalho.objects.all()
        
        # Filtrar baseado no tipo de usuário
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'aluno':
                aluno = Aluno.objects.get(usuario=self.request.user)
                queryset = queryset.filter(aluno=aluno)
            elif perfil.tipo_usuario == 'professor':
                from apps.professores.models import Professor
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(
                    trabalho__turma_disciplina__professor=professor
                )
            elif perfil.tipo_usuario == 'administrador':
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        trabalho__turma_disciplina__turma__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Aluno.DoesNotExist):
            pass
            
        return queryset


class NotaListView(generics.ListCreateAPIView):
    """Lista e cria notas"""
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['aluno', 'turma_disciplina', 'tipo']
    ordering_fields = ['data_avaliacao', 'valor']
    
    def get_queryset(self):
        queryset = Nota.objects.all()
        
        # Filtrar baseado no tipo de usuário
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'professor':
                from apps.professores.models import Professor
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(
                    turma_disciplina__professor=professor
                )
            elif perfil.tipo_usuario == 'administrador':
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        turma_disciplina__turma__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Aluno.DoesNotExist):
            pass
            
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotaCreateSerializer
        return NotaSerializer


class NotaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualiza e remove nota"""
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrAdmin]
    
    def get_queryset(self):
        queryset = Nota.objects.all()
        
        # Filtrar baseado no tipo de usuário
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.tipo_usuario == 'professor':
                from apps.professores.models import Professor
                professor = Professor.objects.get(usuario=self.request.user)
                queryset = queryset.filter(
                    turma_disciplina__professor=professor
                )
            elif perfil.tipo_usuario == 'administrador':
                if perfil.unidade_escolar:
                    queryset = queryset.filter(
                        turma_disciplina__turma__unidade_escolar=perfil.unidade_escolar
                    )
        except (Perfil.DoesNotExist, Aluno.DoesNotExist):
            pass
            
        return queryset


# Views específicas para alunos
class AlunoNotasView(generics.ListAPIView):
    """Lista notas do aluno logado"""
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAluno]
    
    def get_queryset(self):
        try:
            aluno = Aluno.objects.get(usuario=self.request.user)
            return Nota.objects.filter(aluno=aluno)
        except Aluno.DoesNotExist:
            return Nota.objects.none()


class AlunoTrabalhosView(generics.ListAPIView):
    """Lista trabalhos do aluno logado"""
    serializer_class = TrabalhoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAluno]
    
    def get_queryset(self):
        try:
            aluno = Aluno.objects.get(usuario=self.request.user)
            turmas_aluno = AlunoTurma.objects.filter(
                aluno=aluno, ativo=True
            ).values_list('turma_id', flat=True)
            return Trabalho.objects.filter(
                turma_disciplina__turma_id__in=turmas_aluno,
                ativo=True
            )
        except Aluno.DoesNotExist:
            return Trabalho.objects.none()
