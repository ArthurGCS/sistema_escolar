from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as DjangoPasswordChangeForm
from django.contrib.auth.models import User
from .models import Perfil, UnidadeEscolar


class UserRegistrationForm(UserCreationForm):
    """Formulário de registro de usuário"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    tipo_usuario = forms.ChoiceField(
        choices=Perfil.TIPO_USUARIO_CHOICES,
        required=True,
        label='Tipo de Usuário'
    )
    unidade_escolar = forms.ModelChoiceField(
        queryset=UnidadeEscolar.objects.filter(ativo=True),
        required=True,
        label='Unidade Escolar'
    )
    telefone = forms.CharField(max_length=20, required=False, label='Telefone')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Criar perfil
            Perfil.objects.create(
                usuario=user,
                tipo_usuario=self.cleaned_data['tipo_usuario'],
                unidade_escolar=self.cleaned_data['unidade_escolar'],
                telefone=self.cleaned_data['telefone']
            )
        
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Formulário de atualização de perfil"""
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Perfil
        fields = ('tipo_usuario', 'unidade_escolar', 'telefone')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.usuario:
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email
    
    def save(self, commit=True):
        perfil = super().save(commit=False)
        
        # Atualizar dados do usuário
        if perfil.usuario:
            perfil.usuario.first_name = self.cleaned_data['first_name']
            perfil.usuario.last_name = self.cleaned_data['last_name']
            perfil.usuario.email = self.cleaned_data['email']
            perfil.usuario.save()
        
        if commit:
            perfil.save()
        
        return perfil


class PasswordChangeForm(DjangoPasswordChangeForm):
    """Formulário de alteração de senha customizado"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
