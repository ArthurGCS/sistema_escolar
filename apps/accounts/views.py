from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import UnidadeEscolar, Perfil
from .serializers import (
    UnidadeEscolarSerializer, UserSerializer, PerfilSerializer,
    RegisterSerializer, LoginSerializer, ChangePasswordSerializer
)


class UnidadeEscolarListView(generics.ListAPIView):
    """
    Lista todas as unidades escolares ativas
    """
    queryset = UnidadeEscolar.objects.filter(ativo=True)
    serializer_class = UnidadeEscolarSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    """
    Registro de novos usuários
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """
    Login de usuários
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            unidade_escolar_id = serializer.validated_data.get('unidade_escolar_id')
            
            user = authenticate(username=username, password=password)
            
            if user:
                try:
                    perfil = Perfil.objects.get(usuario=user)
                    
                    # Verificar se a unidade escolar foi especificada e é válida
                    if unidade_escolar_id:
                        try:
                            unidade_escolar = UnidadeEscolar.objects.get(
                                id=unidade_escolar_id, 
                                ativo=True
                            )
                            # Atualizar a unidade escolar do perfil se necessário
                            if perfil.unidade_escolar != unidade_escolar:
                                perfil.unidade_escolar = unidade_escolar
                                perfil.save()
                        except UnidadeEscolar.DoesNotExist:
                            return Response(
                                {'error': 'Unidade escolar não encontrada ou inativa'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    
                    # Gerar tokens JWT
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'tipo_usuario': perfil.tipo_usuario,
                            'unidade_escolar': UnidadeEscolarSerializer(perfil.unidade_escolar).data
                        }
                    })
                    
                except Perfil.DoesNotExist:
                    return Response(
                        {'error': 'Perfil de usuário não encontrado'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Credenciais inválidas'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Visualizar e atualizar perfil do usuário
    """
    serializer_class = PerfilSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Perfil, usuario=self.request.user)


class ChangePasswordView(APIView):
    """
    Alterar senha do usuário
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Verificar senha atual
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'error': 'Senha atual incorreta'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Definir nova senha
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': 'Senha alterada com sucesso'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout do usuário
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout realizado com sucesso'})
    except Exception:
        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)


class UnidadeEscolarDetailView(generics.RetrieveAPIView):
    """
    Detalhes de uma unidade escolar específica
    """
    queryset = UnidadeEscolar.objects.filter(ativo=True)
    serializer_class = UnidadeEscolarSerializer
    permission_classes = [permissions.IsAuthenticated]
