from django.contrib import admin
from .models import Especialidad, MedicoLanding

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']

@admin.register(MedicoLanding)
class MedicoLandingAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especialidad', 'activo']