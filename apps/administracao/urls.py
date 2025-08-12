from django.urls import path
from .views import (
    RequerimentoListView, RequerimentoDetailView, ConfiguracaoSistemaListView,
    ConfiguracaoSistemaDetailView, LogSistemaListView, EstatisticasGeraisView,
    EstatisticasUnidadeView, RequerimentoEstatisticasView, criar_log
)

app_name = 'administracao'

urlpatterns = [
    # Requerimentos
    path('requerimentos/', RequerimentoListView.as_view(), name='requerimento-list'),
    path('requerimentos/<int:pk>/', RequerimentoDetailView.as_view(), name='requerimento-detail'),
    
    # Configurações do Sistema
    path('configuracoes/', ConfiguracaoSistemaListView.as_view(), name='configuracao-list'),
    path('configuracoes/<int:pk>/', ConfiguracaoSistemaDetailView.as_view(), name='configuracao-detail'),
    
    # Logs do Sistema
    path('logs/', LogSistemaListView.as_view(), name='log-list'),
    path('logs/criar/', criar_log, name='criar-log'),
    
    # Estatísticas e Relatórios
    path('estatisticas-gerais/', EstatisticasGeraisView.as_view(), name='estatisticas-gerais'),
    path('estatisticas-unidade/<int:unidade_id>/', EstatisticasUnidadeView.as_view(), name='estatisticas-unidade'),
    path('estatisticas-requerimentos/', RequerimentoEstatisticasView.as_view(), name='estatisticas-requerimentos'),
]
