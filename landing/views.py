from django.shortcuts import render
from .models import Especialidad, MedicoLanding

def landing_page(request):
    especialidades = Especialidad.objects.filter(activo=True)
    medicos = MedicoLanding.objects.filter(activo=True)
    return render(request, 'landing/landing.html', {
        'especialidades': especialidades,
        'medicos': medicos,
    })
