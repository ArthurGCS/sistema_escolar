from django.urls import path
from .views import (
    ProfessorListView, ProfessorDetailView, DisciplinaListView, DisciplinaDetailView,
    ProfessorDisciplinaListView, ProfessorDisciplinaDetailView, TurmaDisciplinaListView,
    TurmaDisciplinaDetailView, ProfessorMinhasDisciplinasView, ProfessorEstatisticasView,
    DisciplinaEstatisticasView, ProfessorTrabalhosView, ProfessorNotasView
)

app_name = 'professores'

urlpatterns = [
    # Professores
    path('', ProfessorListView.as_view(), name='professor-list'),
    path('<int:pk>/', ProfessorDetailView.as_view(), name='professor-detail'),
    
    # Disciplinas
    path('disciplinas/', DisciplinaListView.as_view(), name='disciplina-list'),
    path('disciplinas/<int:pk>/', DisciplinaDetailView.as_view(), name='disciplina-detail'),
    
    # Relacionamentos Professor-Disciplina
    path('professor-disciplinas/', ProfessorDisciplinaListView.as_view(), name='professor-disciplina-list'),
    path('professor-disciplinas/<int:pk>/', ProfessorDisciplinaDetailView.as_view(), name='professor-disciplina-detail'),
    
    # Relacionamentos Turma-Disciplina
    path('turma-disciplinas/', TurmaDisciplinaListView.as_view(), name='turma-disciplina-list'),
    path('turma-disciplinas/<int:pk>/', TurmaDisciplinaDetailView.as_view(), name='turma-disciplina-detail'),
    
    # Views específicas para professores
    path('minhas-disciplinas/', ProfessorMinhasDisciplinasView.as_view(), name='minhas-disciplinas'),
    path('estatisticas/', ProfessorEstatisticasView.as_view(), name='estatisticas'),
    path('disciplinas/<int:disciplina_id>/estatisticas/', DisciplinaEstatisticasView.as_view(), name='disciplina-estatisticas'),
    
    # Trabalhos e Notas do professor
    path('trabalhos/', ProfessorTrabalhosView.as_view(), name='trabalhos'),
    path('notas/', ProfessorNotasView.as_view(), name='notas'),
]
