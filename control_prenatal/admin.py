from django.contrib import admin
from .models import HistoriaClinica, ControlPrenatal

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'medico', 'fecha_registro', 'imc_inicial']
    list_filter = ['fecha_registro']
    search_fields = ['paciente__first_name', 'paciente__last_name', 'paciente__username']
    readonly_fields = ['fecha_registro', 'imc_inicial']

@admin.register(ControlPrenatal)
class ControlPrenatalAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'medico', 'fecha', 'semanas_gestacion', 'peso']
    list_filter = ['fecha', 'semanas_gestacion']
    search_fields = ['paciente__first_name', 'paciente__last_name', 'paciente__username']
    readonly_fields = ['fecha']