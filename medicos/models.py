from django.db import models
from usuarios.models import Usuario
from landing.models import Especialidad


class Medico(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    telefono = models.CharField(max_length=10)

    def __str__(self):
        return f"Dr. {self.usuario.first_name} {self.usuario.last_name}"