from django import template
from django.utils import timezone
from datetime import timedelta
from citas.models import Cita

register = template.Library()

@register.simple_tag
def citas_confirmadas_recientes(user):
    """
    Retorna citas confirmadas recientemente (últimas 24h) para el usuario.
    Uso: {% citas_confirmadas_recientes as citas %}
    """
    ahora = timezone.now()
    hace_24h = ahora - timedelta(hours=24)
    
    citas = Cita.objects.filter(
        paciente=user,
        estado='confirmada',
        creado__gte=hace_24h
    ).order_by('-creado')[:3]  # Mostrar máximo 3 citas recientes
    
    return citas
