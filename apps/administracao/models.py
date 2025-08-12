from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStampedModel
from apps.accounts.models import UnidadeEscolar
from apps.professores.models import Professor


class Requerimento(TimeStampedModel):
    """
    Modelo para representar os requerimentos solicitados pelos professores
    """
    TIPO_CHOICES = [
        ('material', 'Material Didático'),
        ('equipamento', 'Equipamento'),
        ('reforma', 'Reforma'),
        ('evento', 'Evento'),
        ('outro', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('concluido', 'Concluído'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, verbose_name='Professor')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='media', verbose_name='Prioridade')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    data_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Solicitação')
    data_resposta = models.DateTimeField(null=True, blank=True, verbose_name='Data de Resposta')
    resposta = models.TextField(blank=True, verbose_name='Resposta')
    administrador_resposta = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Administrador que Respondeu'
    )
    
    class Meta:
        verbose_name = 'Requerimento'
        verbose_name_plural = 'Requerimentos'
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.professor} ({self.get_status_display()})"


class ConfiguracaoSistema(TimeStampedModel):
    """
    Modelo para configurações gerais do sistema
    """
    unidade_escolar = models.OneToOneField(UnidadeEscolar, on_delete=models.CASCADE, verbose_name='Unidade Escolar')
    ano_letivo_atual = models.IntegerField(verbose_name='Ano Letivo Atual')
    periodo_inscricao_aberto = models.BooleanField(default=False, verbose_name='Período de Inscrição Aberto')
    data_inicio_ano_letivo = models.DateField(verbose_name='Data de Início do Ano Letivo')
    data_fim_ano_letivo = models.DateField(verbose_name='Data de Fim do Ano Letivo')
    max_alunos_por_turma = models.IntegerField(default=40, verbose_name='Máximo de Alunos por Turma')
    nota_minima_aprovacao = models.DecimalField(max_digits=3, decimal_places=1, default=6.0, verbose_name='Nota Mínima para Aprovação')
    
    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'
    
    def __str__(self):
        return f"Configuração - {self.unidade_escolar} ({self.ano_letivo_atual})"


class LogSistema(TimeStampedModel):
    """
    Modelo para registrar logs de atividades do sistema
    """
    TIPO_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('criacao', 'Criação'),
        ('edicao', 'Edição'),
        ('exclusao', 'Exclusão'),
        ('visualizacao', 'Visualização'),
        ('erro', 'Erro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    acao = models.CharField(max_length=200, verbose_name='Ação')
    detalhes = models.TextField(blank=True, verbose_name='Detalhes')
    ip_address = models.GenericIPAddressField(verbose_name='Endereço IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    class Meta:
        verbose_name = 'Log do Sistema'
        verbose_name_plural = 'Logs do Sistema'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.usuario} - {self.get_tipo_display()}: {self.acao}"
