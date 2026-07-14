from django.contrib import admin
from .models import PrediccionIA


@admin.register(PrediccionIA)
class PrediccionIAAdmin(admin.ModelAdmin):
    list_display   = ('paciente', 'nivel_riesgo', 'puntuacion_riesgo', 'semanas_gestacion', 'fecha')
    list_filter    = ('nivel_riesgo', 'fecha')
    search_fields  = ('paciente__usuario__first_name', 'paciente__usuario__last_name')
    readonly_fields = ('fecha', 'resultado')
    ordering       = ('-fecha',)
