from django import template
from collections import defaultdict, OrderedDict

register = template.Library()


@register.filter
def agrupar_por_mes(controles):
    """
    Agrupa controles por mes en orden descendente (más recientes primero).
    
    Retorna un OrderedDict con estructura:
    {
        'YYYY-MM': {
            'mes': 'Julio 2026',
            'controles': [...]
        },
        ...
    }
    """
    if not controles:
        return OrderedDict()
    
    # Agrupar por mes-año
    grupos = {}
    for control in controles:
        mes_key = control.fecha.strftime('%Y-%m')
        if mes_key not in grupos:
            # Usar strftime directamente en lugar de format_date (compatible con Django 5.2)
            grupos[mes_key] = {
                'mes': control.fecha.strftime('%B %Y'),
                'controles': []
            }
        grupos[mes_key]['controles'].append(control)
    
    # Ordenar en forma descendente (más recientes primero)
    grupos_ordenados = OrderedDict(sorted(grupos.items(), reverse=True))
    
    return grupos_ordenados
