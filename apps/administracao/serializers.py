from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Requerimento, ConfiguracaoSistema, LogSistema
from apps.accounts.models import UnidadeEscolar
from apps.professores.models import Professor


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UnidadeEscolarSerializer(serializers.ModelSerializer):
    """Serializer para UnidadeEscolar"""
    class Meta:
        model = UnidadeEscolar
        fields = ['id', 'nome', 'endereco', 'telefone', 'email']


class ProfessorSerializer(serializers.ModelSerializer):
    """Serializer para Professor"""
    usuario = UserSerializer(read_only=True)
    
    class Meta:
        model = Professor
        fields = ['id', 'matricula', 'usuario', 'formacao', 'status']


class RequerimentoSerializer(serializers.ModelSerializer):
    """Serializer para Requerimento"""
    professor = ProfessorSerializer(read_only=True)
    administrador_resposta = UserSerializer(read_only=True)
    
    class Meta:
        model = Requerimento
        fields = [
            'id', 'titulo', 'descricao', 'professor', 'tipo', 'prioridade',
            'status', 'data_solicitacao', 'data_resposta', 'resposta',
            'administrador_resposta'
        ]


class RequerimentoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Requerimento"""
    class Meta:
        model = Requerimento
        fields = ['titulo', 'descricao', 'tipo', 'prioridade']


class RequerimentoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de Requerimento (administração)"""
    class Meta:
        model = Requerimento
        fields = ['status', 'resposta']


class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    """Serializer para ConfiguracaoSistema"""
    unidade_escolar = UnidadeEscolarSerializer(read_only=True)
    
    class Meta:
        model = ConfiguracaoSistema
        fields = [
            'id', 'unidade_escolar', 'ano_letivo_atual', 'periodo_inscricao_aberto',
            'data_inicio_ano_letivo', 'data_fim_ano_letivo', 'max_alunos_por_turma',
            'nota_minima_aprovacao'
        ]


class ConfiguracaoSistemaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de ConfiguracaoSistema"""
    class Meta:
        model = ConfiguracaoSistema
        fields = [
            'unidade_escolar', 'ano_letivo_atual', 'periodo_inscricao_aberto',
            'data_inicio_ano_letivo', 'data_fim_ano_letivo', 'max_alunos_por_turma',
            'nota_minima_aprovacao'
        ]


class LogSistemaSerializer(serializers.ModelSerializer):
    """Serializer para LogSistema"""
    usuario = UserSerializer(read_only=True)
    
    class Meta:
        model = LogSistema
        fields = [
            'id', 'usuario', 'tipo', 'acao', 'detalhes', 'ip_address',
            'user_agent', 'created_at'
        ]


# Serializers para relatórios e estatísticas
class EstatisticasGeraisSerializer(serializers.Serializer):
    """Serializer para estatísticas gerais do sistema"""
    total_alunos = serializers.IntegerField()
    total_professores = serializers.IntegerField()
    total_turmas = serializers.IntegerField()
    total_disciplinas = serializers.IntegerField()
    total_requerimentos_pendentes = serializers.IntegerField()
    total_trabalhos_ativos = serializers.IntegerField()


class EstatisticasUnidadeSerializer(serializers.Serializer):
    """Serializer para estatísticas de uma unidade específica"""
    unidade = UnidadeEscolarSerializer()
    total_alunos = serializers.IntegerField()
    total_professores = serializers.IntegerField()
    total_turmas = serializers.IntegerField()
    media_notas = serializers.FloatField()
    requerimentos_pendentes = serializers.IntegerField()


class RequerimentoEstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas de requerimentos"""
    total_requerimentos = serializers.IntegerField()
    requerimentos_pendentes = serializers.IntegerField()
    requerimentos_aprovados = serializers.IntegerField()
    requerimentos_rejeitados = serializers.IntegerField()
    requerimentos_por_tipo = serializers.DictField()
    requerimentos_por_prioridade = serializers.DictField()
