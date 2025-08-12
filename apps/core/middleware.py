from django.utils.deprecation import MiddlewareMixin
from apps.accounts.models import UnidadeEscolar, Perfil


class UnidadeEscolarMiddleware(MiddlewareMixin):
    """
    Middleware para gerenciar a unidade escolar na sessão
    """
    
    def process_request(self, request):
        # Adicionar a unidade escolar atual à requisição
        request.unidade_escolar_atual = None
        
        if request.user.is_authenticated:
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                request.unidade_escolar_atual = perfil.unidade_escolar
            except Perfil.DoesNotExist:
                pass
        
        return None
