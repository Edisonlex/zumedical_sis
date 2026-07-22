from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, LogAuditoria
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


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'modulo', 'severidad', 'ip_address')
    list_filter = ('accion', 'severidad', 'modulo', 'fecha')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'descripcion', 'modulo', 'ip_address')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)
    list_per_page = 50
    
    readonly_fields = ('usuario', 'accion', 'modulo', 'descripcion', 'ip_address', 'severidad', 'fecha')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
admin.site.register(Usuario, UsuarioAdmin)