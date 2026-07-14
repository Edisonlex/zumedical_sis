from django.db import models
from django.conf import settings

ESTADO_EMBARAZO_CHOICES = (
    ('NINGUNO', 'Ninguno'),
    ('ACTIVO', 'Activo'),
    ('FINALIZADO', 'Finalizado'),
    ('SUSPENDIDO', 'Suspendido'),
)

class Paciente(models.Model):

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paciente',
    )

    cedula = models.CharField(max_length=10, blank=True, default='')
    edad = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=200, blank=True, default='')
    telefono = models.CharField(max_length=10, blank=True, default='')
    fecha_ultima_menstruacion = models.DateField(null=True, blank=True)
    fecha_probable_parto = models.DateField(null=True, blank=True)

    # Módulo prenatal activable para pacientes (reemplaza tiene_prenatal)
    estado_embarazo = models.CharField(
        max_length=20,
        choices=ESTADO_EMBARAZO_CHOICES,
        default='NINGUNO',
        verbose_name='Estado del Embarazo',
        help_text='Indica si la paciente tiene un embarazo en curso, finalizado, etc.'
    )

    mensaje_prenatal_visto = models.BooleanField(
        default=False,
        verbose_name='Mensaje Prenatal Visto',
        help_text='Indica si la paciente ya vio el mensaje de bienvenida al panel prenatal'
    )

    # Médico prenatal responsable — se asigna cuando el médico activa el embarazo
    medico_prenatal = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes_prenatales',
        verbose_name='Médico prenatal responsable',
        help_text='Médico que activó y lleva el seguimiento del embarazo',
    )

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} ({self.usuario.username})"