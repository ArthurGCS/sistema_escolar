from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UnidadeEscolar, Perfil


class UnidadeEscolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeEscolar
        fields = ['id', 'nome', 'endereco', 'telefone', 'email', 'ativo']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    unidade_escolar = UnidadeEscolarSerializer(read_only=True)
    unidade_escolar_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Perfil
        fields = [
            'id', 'usuario', 'tipo_usuario', 'telefone', 
            'unidade_escolar', 'unidade_escolar_id'
        ]
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    tipo_usuario = serializers.ChoiceField(choices=Perfil.TIPO_USUARIO_CHOICES, required=True)
    unidade_escolar_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'first_name', 'last_name', 
            'email', 'tipo_usuario', 'unidade_escolar_id'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        tipo_usuario = validated_data.pop('tipo_usuario')
        unidade_escolar_id = validated_data.pop('unidade_escolar_id')
        
        user = User.objects.create_user(**validated_data)
        
        try:
            unidade_escolar = UnidadeEscolar.objects.get(id=unidade_escolar_id)
        except UnidadeEscolar.DoesNotExist:
            raise serializers.ValidationError({"unidade_escolar_id": "Unidade escolar não encontrada."})
        
        Perfil.objects.create(
            usuario=user,
            tipo_usuario=tipo_usuario,
            unidade_escolar=unidade_escolar
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    unidade_escolar_id = serializers.IntegerField(required=False)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
