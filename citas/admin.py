from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'especialidad', 'fecha', 'hora', 'estado', 'creado')
    list_filter = ('estado', 'fecha', 'especialidad', 'medico')
    search_fields = ('paciente__username', 'paciente__first_name', 'paciente__last_name', 
                     'medico__username', 'medico__first_name', 'medico__last_name', 'motivo')
    date_hierarchy = 'fecha'
    ordering = ('-fecha', '-hora')
    list_per_page = 25
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('paciente', 'medico', 'especialidad')
        }),
        ('Detalles de la Cita', {
            'fields': ('fecha', 'hora', 'motivo', 'estado')
        }),
        ('Cancelación', {
            'fields': ('motivo_cancelacion',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('creado',)
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar desde el admin, solo cancelar
        return False