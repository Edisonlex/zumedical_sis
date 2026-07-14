"""
context_processors.py — Zumedical
Inyecta variables globales al contexto de todos los templates.
"""


def medico_context(request):
    """
    Disponible en todos los templates:
        es_prenatal      — bool: True si el médico logueado es de especialidad prenatal
        sb_citas_pendientes — int: citas pendientes del médico hoy (para el badge del sidebar)
    """
    if not request.user.is_authenticated or request.user.rol != 'medico':
        return {}

    # Determinar tipo de médico
    try:
        es_prenatal = (
            request.user.medico.especialidad is not None and
            request.user.medico.especialidad.tipo == 'prenatal'
        )
    except Exception:
        es_prenatal = False

    # Badge de citas pendientes (hoy)
    try:
        from django.utils import timezone
        from citas.models import Cita
        hoy = timezone.now().date()
        sb_citas_pendientes = Cita.objects.filter(
            medico=request.user,
            estado='pendiente',
            fecha=hoy,
        ).count()
    except Exception:
        sb_citas_pendientes = 0

    return {
        'es_prenatal':         es_prenatal,
        'sb_citas_pendientes': sb_citas_pendientes,
    }
