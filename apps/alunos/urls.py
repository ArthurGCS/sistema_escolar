from django.urls import path
from .views import (
    AlunoListView, AlunoDetailView, TurmaListView, TurmaDetailView,
    AlunoTurmaListView, AlunoTurmaDetailView, TrabalhoListView, TrabalhoDetailView,
    EntregaTrabalhoListView, EntregaTrabalhoDetailView, NotaListView, NotaDetailView,
    AlunoNotasView, AlunoTrabalhosView
)

app_name = 'alunos'

urlpatterns = [
    # Alunos
    path('', AlunoListView.as_view(), name='aluno-list'),
    path('<int:pk>/', AlunoDetailView.as_view(), name='aluno-detail'),
    
    # Turmas
    path('turmas/', TurmaListView.as_view(), name='turma-list'),
    path('turmas/<int:pk>/', TurmaDetailView.as_view(), name='turma-detail'),
    
    # Relacionamentos Aluno-Turma
    path('aluno-turmas/', AlunoTurmaListView.as_view(), name='aluno-turma-list'),
    path('aluno-turmas/<int:pk>/', AlunoTurmaDetailView.as_view(), name='aluno-turma-detail'),
    
    # Trabalhos
    path('trabalhos/', TrabalhoListView.as_view(), name='trabalho-list'),
    path('trabalhos/<int:pk>/', TrabalhoDetailView.as_view(), name='trabalho-detail'),
    
    # Entregas de Trabalhos
    path('entregas/', EntregaTrabalhoListView.as_view(), name='entrega-list'),
    path('entregas/<int:pk>/', EntregaTrabalhoDetailView.as_view(), name='entrega-detail'),
    
    # Notas
    path('notas/', NotaListView.as_view(), name='nota-list'),
    path('notas/<int:pk>/', NotaDetailView.as_view(), name='nota-detail'),
    
    # Views específicas para alunos
    path('minhas-notas/', AlunoNotasView.as_view(), name='minhas-notas'),
    path('meus-trabalhos/', AlunoTrabalhosView.as_view(), name='meus-trabalhos'),
]
