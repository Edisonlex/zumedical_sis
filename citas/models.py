from django.db import models
from django.conf import settings
from landing.models import Especialidad


class Cita(models.Model):

    ESTADO = (
        ('pendiente',  'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('atendido',   'Atendido'),
        ('cancelado',  'Cancelado'),
    )

    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citas_paciente',
        limit_choices_to={'rol': 'paciente'}
    )

    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citas_medico',
        limit_choices_to={'rol': 'medico'}
    )

    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=255)
    motivo_cancelacion = models.TextField(blank=True, null=True, help_text="Motivo de cancelación de la cita")

    estado = models.CharField(
        max_length=20,
        choices=ESTADO,
        default='pendiente'
    )

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita: {self.paciente} - {self.medico} - {self.fecha} {self.hora}"

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        unique_together = ('medico', 'fecha', 'hora')
        ordering = ['-fecha', '-hora']