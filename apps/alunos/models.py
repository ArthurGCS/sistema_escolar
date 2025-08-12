from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStampedModel
from apps.accounts.models import UnidadeEscolar


class Aluno(TimeStampedModel):
    """
    Modelo para representar os alunos
    """
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('transferido', 'Transferido'),
        ('concluido', 'Concluído'),
    ]
    
    matricula = models.CharField(max_length=20, unique=True, verbose_name='Matrícula')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    unidade_escolar = models.ForeignKey(UnidadeEscolar, on_delete=models.CASCADE, verbose_name='Unidade Escolar')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name='Sexo')
    endereco = models.TextField(verbose_name='Endereço')
    nome_responsavel = models.CharField(max_length=200, verbose_name='Nome do Responsável')
    telefone_responsavel = models.CharField(max_length=20, verbose_name='Telefone do Responsável')
    email_responsavel = models.EmailField(blank=True, verbose_name='E-mail do Responsável')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['usuario__first_name', 'usuario__last_name']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.matricula}"


class Turma(TimeStampedModel):
    """
    Modelo para representar as turmas
    """
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
        ('integral', 'Integral'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name='Nome da Turma')
    unidade_escolar = models.ForeignKey(UnidadeEscolar, on_delete=models.CASCADE, verbose_name='Unidade Escolar')
    ano = models.IntegerField(verbose_name='Ano')
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, verbose_name='Turno')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        unique_together = ['nome', 'unidade_escolar', 'ano']
        ordering = ['ano', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.ano} ({self.get_turno_display()})"


class AlunoTurma(TimeStampedModel):
    """
    Modelo para relacionar alunos com turmas
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    data_entrada = models.DateField(auto_now_add=True, verbose_name='Data de Entrada')
    data_saida = models.DateField(null=True, blank=True, verbose_name='Data de Saída')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Aluno na Turma'
        verbose_name_plural = 'Alunos nas Turmas'
        unique_together = ['aluno', 'turma']
    
    def __str__(self):
        return f"{self.aluno} - {self.turma}"


class Trabalho(TimeStampedModel):
    """
    Modelo para representar os trabalhos acadêmicos
    """
    TIPO_CHOICES = [
        ('individual', 'Individual'),
        ('grupo', 'Grupo'),
        ('projeto', 'Projeto'),
        ('pesquisa', 'Pesquisa'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    turma_disciplina = models.ForeignKey('professores.TurmaDisciplina', on_delete=models.CASCADE, verbose_name='Turma/Disciplina')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    data_entrega = models.DateField(verbose_name='Data de Entrega')
    valor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Valor (pontos)')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Trabalho'
        verbose_name_plural = 'Trabalhos'
        ordering = ['-data_entrega']
    
    def __str__(self):
        return f"{self.titulo} - {self.turma_disciplina}"


class EntregaTrabalho(TimeStampedModel):
    """
    Modelo para representar as entregas de trabalhos pelos alunos
    """
    trabalho = models.ForeignKey(Trabalho, on_delete=models.CASCADE, verbose_name='Trabalho')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    arquivo = models.FileField(upload_to='trabalhos/', verbose_name='Arquivo')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Nota')
    data_entrega = models.DateTimeField(auto_now_add=True, verbose_name='Data de Entrega')
    
    class Meta:
        verbose_name = 'Entrega de Trabalho'
        verbose_name_plural = 'Entregas de Trabalhos'
        unique_together = ['trabalho', 'aluno']
    
    def __str__(self):
        return f"{self.aluno} - {self.trabalho}"


class Nota(TimeStampedModel):
    """
    Modelo para representar as notas dos alunos
    """
    TIPO_CHOICES = [
        ('prova1', 'Prova 1'),
        ('prova2', 'Prova 2'),
        ('prova3', 'Prova 3'),
        ('prova4', 'Prova 4'),
        ('recuperacao', 'Recuperação'),
        ('trabalho', 'Trabalho'),
        ('participacao', 'Participação'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    turma_disciplina = models.ForeignKey('professores.TurmaDisciplina', on_delete=models.CASCADE, verbose_name='Turma/Disciplina')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    valor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Valor')
    data_avaliacao = models.DateField(verbose_name='Data da Avaliação')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ['aluno', 'turma_disciplina', 'tipo']
        ordering = ['-data_avaliacao']
    
    def __str__(self):
        return f"{self.aluno} - {self.turma_disciplina} - {self.get_tipo_display()}: {self.valor}"
