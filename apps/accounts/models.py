from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStampedModel


class UnidadeEscolar(TimeStampedModel):
    """
    Modelo para representar as unidades escolares
    """
    nome = models.CharField(max_length=200, verbose_name='Nome da Unidade')
    endereco = models.TextField(verbose_name='Endereço')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Unidade Escolar'
        verbose_name_plural = 'Unidades Escolares'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Perfil(TimeStampedModel):
    """
    Modelo para estender o usuário com informações adicionais
    """
    TIPO_USUARIO_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('administrador', 'Administrador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, verbose_name='Tipo de Usuário')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    unidade_escolar = models.ForeignKey(
        UnidadeEscolar, 
        on_delete=models.CASCADE, 
        verbose_name='Unidade Escolar',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_tipo_usuario_display()}"
