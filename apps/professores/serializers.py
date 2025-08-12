from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Professor, Disciplina, ProfessorDisciplina, TurmaDisciplina
from apps.accounts.models import UnidadeEscolar
from apps.alunos.models import Turma


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


class ProfessorSerializer(serializers.ModelSerializer):
    """Serializer para Professor"""
    usuario = UserSerializer(read_only=True)
    unidade_escolar = UnidadeEscolarSerializer(read_only=True)
    disciplinas = serializers.StringRelatedField(many=True, source='professordisciplina_set')
    
    class Meta:
        model = Professor
        fields = [
            'id', 'matricula', 'usuario', 'unidade_escolar', 'data_nascimento',
            'sexo', 'endereco', 'telefone', 'email', 'formacao', 'status',
            'disciplinas'
        ]


class ProfessorCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Professor"""
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = Professor
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'matricula', 'unidade_escolar', 'data_nascimento', 'sexo',
            'endereco', 'telefone', 'email', 'formacao'
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
        
        # Criar professor
        professor = Professor.objects.create(usuario=user, **validated_data)
        
        return professor


class DisciplinaSerializer(serializers.ModelSerializer):
    """Serializer para Disciplina"""
    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'codigo', 'descricao', 'carga_horaria', 'ativa']


class ProfessorDisciplinaSerializer(serializers.ModelSerializer):
    """Serializer para ProfessorDisciplina"""
    professor = ProfessorSerializer(read_only=True)
    disciplina = DisciplinaSerializer(read_only=True)
    
    class Meta:
        model = ProfessorDisciplina
        fields = ['id', 'professor', 'disciplina', 'ativo']


class ProfessorDisciplinaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de ProfessorDisciplina"""
    class Meta:
        model = ProfessorDisciplina
        fields = ['professor', 'disciplina']


class TurmaDisciplinaSerializer(serializers.ModelSerializer):
    """Serializer para TurmaDisciplina"""
    turma = TurmaSerializer(read_only=True)
    disciplina = DisciplinaSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)
    
    class Meta:
        model = TurmaDisciplina
        fields = [
            'id', 'turma', 'disciplina', 'professor', 'carga_horaria_semanal', 'ativo'
        ]


class TurmaDisciplinaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de TurmaDisciplina"""
    class Meta:
        model = TurmaDisciplina
        fields = ['turma', 'disciplina', 'professor', 'carga_horaria_semanal']


# Serializers para relatórios e estatísticas
class ProfessorEstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas do professor"""
    total_disciplinas = serializers.IntegerField()
    total_turmas = serializers.IntegerField()
    total_alunos = serializers.IntegerField()
    trabalhos_pendentes = serializers.IntegerField()
    notas_para_lancar = serializers.IntegerField()


class DisciplinaEstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas da disciplina"""
    disciplina = DisciplinaSerializer()
    total_turmas = serializers.IntegerField()
    total_alunos = serializers.IntegerField()
    media_notas = serializers.FloatField()
    trabalhos_ativos = serializers.IntegerField()
