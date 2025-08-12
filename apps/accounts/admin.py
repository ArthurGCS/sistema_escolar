from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UnidadeEscolar, Perfil


@admin.register(UnidadeEscolar)
class UnidadeEscolarAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco', 'telefone', 'email', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'endereco', 'email']
    ordering = ['nome']


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo_usuario', 'unidade_escolar', 'telefone']
    list_filter = ['tipo_usuario', 'unidade_escolar']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name']
    ordering = ['usuario__first_name']


# Personalizar o admin do User para incluir informações do perfil
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'


class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_tipo_usuario']
    
    def get_tipo_usuario(self, obj):
        try:
            return obj.perfil.tipo_usuario
        except Perfil.DoesNotExist:
            return 'N/A'
    get_tipo_usuario.short_description = 'Tipo de Usuário'


# Re-registrar o User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
