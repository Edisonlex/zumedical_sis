from django.db import models

class Especialidad(models.Model):
    TIPO_CHOICES = [
        ('prenatal', 'Prenatal'),
        ('general', 'General'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, help_text="Clase de ícono Font Awesome, ej: fa-heartbeat")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='general')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class MedicoLanding(models.Model):
    nombre = models.CharField(max_length=150)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)
    foto = models.ImageField(upload_to='medicos_landing/', blank=True, null=True)
    descripcion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Médico Landing"
        verbose_name_plural = "Médicos Landing"

    def __str__(self):
        return self.nombre