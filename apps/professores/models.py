from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStampedModel
from apps.accounts.models import UnidadeEscolar


class Professor(TimeStampedModel):
    """
    Modelo para representar os professores
    """
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('licenca', 'Licença'),
        ('aposentado', 'Aposentado'),
    ]
    
    matricula = models.CharField(max_length=20, unique=True, verbose_name='Matrícula')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    unidade_escolar = models.ForeignKey(UnidadeEscolar, on_delete=models.CASCADE, verbose_name='Unidade Escolar')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name='Sexo')
    endereco = models.TextField(verbose_name='Endereço')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    email = models.EmailField(verbose_name='E-mail')
    formacao = models.CharField(max_length=200, verbose_name='Formação')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')
    
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
        ordering = ['usuario__first_name', 'usuario__last_name']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.matricula}"


class Disciplina(TimeStampedModel):
    """
    Modelo para representar as disciplinas
    """
    nome = models.CharField(max_length=100, verbose_name='Nome da Disciplina')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    carga_horaria = models.IntegerField(verbose_name='Carga Horária (horas)')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    
    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.codigo})"


class ProfessorDisciplina(TimeStampedModel):
    """
    Modelo para relacionar professores com disciplinas
    """
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, verbose_name='Professor')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name='Disciplina')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Professor na Disciplina'
        verbose_name_plural = 'Professores nas Disciplinas'
        unique_together = ['professor', 'disciplina']
    
    def __str__(self):
        return f"{self.professor} - {self.disciplina}"


class TurmaDisciplina(TimeStampedModel):
    """
    Modelo para relacionar turmas com disciplinas e professores
    """
    turma = models.ForeignKey('alunos.Turma', on_delete=models.CASCADE, verbose_name='Turma')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name='Disciplina')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, verbose_name='Professor')
    carga_horaria_semanal = models.IntegerField(verbose_name='Carga Horária Semanal (horas)')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Disciplina na Turma'
        verbose_name_plural = 'Disciplinas nas Turmas'
        unique_together = ['turma', 'disciplina']
    
    def __str__(self):
        return f"{self.turma} - {self.disciplina} ({self.professor})"
