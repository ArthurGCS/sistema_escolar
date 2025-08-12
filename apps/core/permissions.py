from rest_framework import permissions
from apps.accounts.models import Perfil


class IsAluno(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é um aluno
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            return perfil.tipo_usuario == 'aluno'
        except Perfil.DoesNotExist:
            return False


class IsProfessor(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é um professor
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            return perfil.tipo_usuario == 'professor'
        except Perfil.DoesNotExist:
            return False


class IsAdministrador(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é um administrador
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            return perfil.tipo_usuario == 'administrador'
        except Perfil.DoesNotExist:
            return False


class IsProfessorOrAdmin(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é professor ou administrador
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            return perfil.tipo_usuario in ['professor', 'administrador']
        except Perfil.DoesNotExist:
            return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é o dono do recurso ou administrador
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            
            # Administradores podem acessar tudo
            if perfil.tipo_usuario == 'administrador':
                return True
            
            # Verificar se o usuário é o dono do recurso
            if hasattr(obj, 'usuario'):
                return obj.usuario == request.user
            elif hasattr(obj, 'aluno') and hasattr(obj.aluno, 'usuario'):
                return obj.aluno.usuario == request.user
            elif hasattr(obj, 'professor') and hasattr(obj.professor, 'usuario'):
                return obj.professor.usuario == request.user
            
            return False
            
        except Perfil.DoesNotExist:
            return False
