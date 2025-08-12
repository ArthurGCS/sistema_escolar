from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Aluno, Turma, AlunoTurma, Trabalho, EntregaTrabalho, Nota
from apps.accounts.models import UnidadeEscolar
from apps.professores.models import TurmaDisciplina


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


class TurmaSerializer(serializers.ModelSerializer):
    """Serializer para Turma"""
    unidade_escolar = UnidadeEscolarSerializer(read_only=True)
    
    class Meta:
        model = Turma
        fields = ['id', 'nome', 'unidade_escolar', 'ano', 'turno', 'ativa']


class AlunoSerializer(serializers.ModelSerializer):
    """Serializer para Aluno"""
    usuario = UserSerializer(read_only=True)
    unidade_escolar = UnidadeEscolarSerializer(read_only=True)
    turmas = TurmaSerializer(many=True, read_only=True, source='alunoturma_set')
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'matricula', 'usuario', 'unidade_escolar', 'data_nascimento',
            'sexo', 'endereco', 'nome_responsavel', 'telefone_responsavel',
            'email_responsavel', 'status', 'turmas'
        ]


class AlunoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Aluno"""
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = Aluno
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'matricula', 'unidade_escolar', 'data_nascimento', 'sexo',
            'endereco', 'nome_responsavel', 'telefone_responsavel',
            'email_responsavel'
        ]
    
    def create(self, validated_data):
        # Extrair dados do usuário
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
        }
        
        # Criar usuário
        user = User.objects.create_user(**user_data)
        
        # Criar aluno
        aluno = Aluno.objects.create(usuario=user, **validated_data)
        
        return aluno


class AlunoTurmaSerializer(serializers.ModelSerializer):
    """Serializer para AlunoTurma"""
    aluno = AlunoSerializer(read_only=True)
    turma = TurmaSerializer(read_only=True)
    
    class Meta:
        model = AlunoTurma
        fields = ['id', 'aluno', 'turma', 'data_entrada', 'data_saida', 'ativo']


class TurmaDisciplinaSerializer(serializers.ModelSerializer):
    """Serializer para TurmaDisciplina"""
    disciplina = serializers.StringRelatedField()
    professor = serializers.StringRelatedField()
    
    class Meta:
        model = TurmaDisciplina
        fields = ['id', 'disciplina', 'professor', 'carga_horaria_semanal']


class TrabalhoSerializer(serializers.ModelSerializer):
    """Serializer para Trabalho"""
    turma_disciplina = TurmaDisciplinaSerializer(read_only=True)
    
    class Meta:
        model = Trabalho
        fields = [
            'id', 'titulo', 'descricao', 'turma_disciplina', 'tipo',
            'data_entrega', 'valor', 'ativo'
        ]


class TrabalhoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Trabalho"""
    class Meta:
        model = Trabalho
        fields = [
            'titulo', 'descricao', 'turma_disciplina', 'tipo',
            'data_entrega', 'valor'
        ]


class EntregaTrabalhoSerializer(serializers.ModelSerializer):
    """Serializer para EntregaTrabalho"""
    trabalho = TrabalhoSerializer(read_only=True)
    aluno = AlunoSerializer(read_only=True)
    
    class Meta:
        model = EntregaTrabalho
        fields = [
            'id', 'trabalho', 'aluno', 'arquivo', 'observacoes',
            'nota', 'data_entrega'
        ]


class EntregaTrabalhoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de EntregaTrabalho"""
    class Meta:
        model = EntregaTrabalho
        fields = ['trabalho', 'arquivo', 'observacoes']


class NotaSerializer(serializers.ModelSerializer):
    """Serializer para Nota"""
    aluno = AlunoSerializer(read_only=True)
    turma_disciplina = TurmaDisciplinaSerializer(read_only=True)
    
    class Meta:
        model = Nota
        fields = [
            'id', 'aluno', 'turma_disciplina', 'tipo', 'valor',
            'data_avaliacao', 'observacoes'
        ]


class NotaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Nota"""
    class Meta:
        model = Nota
        fields = ['aluno', 'turma_disciplina', 'tipo', 'valor', 'data_avaliacao', 'observacoes']
