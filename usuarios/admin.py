from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from pacientes.models import Paciente
from medicos.models import Medico


class PacienteInline(admin.StackedInline):
    model = Paciente
    can_delete = False
    verbose_name_plural = 'Perfil Paciente'
    extra = 0


class MedicoInline(admin.StackedInline):
    model = Medico
    can_delete = False
    verbose_name_plural = 'Perfil Médico'
    extra = 0


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'rol', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.rol == 'paciente':
                return [PacienteInline]
            elif obj.rol == 'medico':
                return [MedicoInline]
        return []
    
admin.site.register(Usuario, UsuarioAdmin)