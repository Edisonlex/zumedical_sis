from django.db import models
from django.conf import settings


class HistoriaClinica(models.Model):
    """
    Historia Clínica Obstétrica — se crea UNA SOLA VEZ por paciente.
    Contiene la anamnesis completa, antecedentes y datos antropométricos iniciales.
    Equivale al formulario físico de Zumedical.
    """
    paciente = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='historia_clinica',
        verbose_name='Paciente',
    )
    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='historias_creadas',
        verbose_name='Médico que registra',
    )
    fecha_registro = models.DateField(auto_now_add=True)

    # ── Antecedentes patológicos personales ───────────────────────────────
    antecedentes_personales = models.TextField(
        blank=True, default='',
        verbose_name='Antecedentes patológicos personales',
        help_text='Enfermedades previas, cirugías, alergias, etc.',
    )

    # ── Antecedentes familiares ────────────────────────────────────────────
    antecedentes_familiares = models.TextField(
        blank=True, default='',
        verbose_name='Antecedentes familiares',
        help_text='Diabetes, hipertensión, gemelos, enfermedades hereditarias',
    )

    # ── Antecedentes obstétricos y ginecológicos ──────────────────────────
    antecedentes_obstetricos = models.TextField(
        blank=True, default='',
        verbose_name='Antecedentes obstétricos y ginecológicos',
        help_text='Partos anteriores, abortos, cesáreas, fecha última regla',
    )
    gestas           = models.IntegerField(default=0, verbose_name='Gestas (G)')
    partos           = models.IntegerField(default=0, verbose_name='Partos (P)')
    cesareas         = models.IntegerField(default=0, verbose_name='Cesáreas (C)')
    abortos          = models.IntegerField(default=0, verbose_name='Abortos (A)')
    hijos_vivos      = models.IntegerField(default=0, verbose_name='Hijos vivos (HV)')

    # ── Motivo de consulta ────────────────────────────────────────────────
    motivo_consulta = models.TextField(
        blank=True, default='',
        verbose_name='Motivo de consulta',
    )

    # ── Score Mamá (signos vitales de la primera consulta) ────────────────
    presion_arterial_inicial    = models.CharField(max_length=20, blank=True, default='', verbose_name='Presión arterial')
    frecuencia_cardiaca_inicial = models.IntegerField(null=True, blank=True, verbose_name='Frecuencia cardíaca (lpm)')
    frecuencia_respiratoria     = models.IntegerField(null=True, blank=True, verbose_name='Frecuencia respiratoria (rpm)')
    temperatura_inicial         = models.FloatField(null=True, blank=True, verbose_name='Temperatura (°F)')
    saturacion_oxigeno          = models.IntegerField(null=True, blank=True, verbose_name='Saturación de oxígeno (%)')
    estado_conciencia           = models.CharField(
        max_length=50, blank=True, default='Alerta',
        verbose_name='Estado de conciencia',
    )
    proteinuria                 = models.CharField(
        max_length=20, blank=True, default='Negativa',
        verbose_name='Proteinuria',
        help_text='Negativa / +1 / +2 / +3',
    )

    # ── Datos antropométricos iniciales ──────────────────────────────────
    peso_inicial  = models.FloatField(null=True, blank=True, verbose_name='Peso inicial (kg)')
    talla         = models.FloatField(null=True, blank=True, verbose_name='Talla (m)')
    imc_inicial   = models.FloatField(null=True, blank=True, verbose_name='IMC preconcepcional')

    # ── Examen físico general ────────────────────────────────────────────
    examen_fisico = models.TextField(
        blank=True, default='',
        verbose_name='Examen físico',
    )

    # ── Evolución y diagnóstico ──────────────────────────────────────────
    evolucion_enfermedad        = models.TextField(blank=True, default='', verbose_name='Evolución de la enfermedad')
    resultado_examenes          = models.TextField(blank=True, default='', verbose_name='Resultado de exámenes complementarios')
    diagnostico                 = models.TextField(blank=True, default='', verbose_name='Diagnóstico')
    tratamiento                 = models.TextField(blank=True, default='', verbose_name='Tratamiento')

    class Meta:
        verbose_name        = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'

    def __str__(self):
        return f"HC — {self.paciente.get_full_name()}"

    def save(self, *args, **kwargs):
        # Calcular IMC automáticamente si hay peso y talla
        if self.peso_inicial and self.talla and self.talla > 0:
            self.imc_inicial = round(self.peso_inicial / (self.talla ** 2), 1)
        super().save(*args, **kwargs)

    @property
    def categoria_imc(self):
        """Categoría de IMC preconcepcional para las curvas de peso."""
        if not self.imc_inicial:
            return None
        if self.imc_inicial < 18.5:
            return 'bajo_peso'
        elif self.imc_inicial < 25:
            return 'normal'
        elif self.imc_inicial < 30:
            return 'sobrepeso'
        else:
            return 'obesidad'

    @property
    def ganancia_recomendada(self):
        """Rango de ganancia de peso total recomendado según IMC (IOM guidelines)."""
        cat = self.categoria_imc
        return {
            'bajo_peso':  (12.5, 18.0),
            'normal':     (11.5, 16.0),
            'sobrepeso':  (7.0,  11.5),
            'obesidad':   (5.0,  9.0),
        }.get(cat, (11.5, 16.0))

    @property
    def formula_obstetrica(self):
        return f"G{self.gestas} P{self.partos} C{self.cesareas} A{self.abortos} HV{self.hijos_vivos}"


class ControlPrenatal(models.Model):
    """
    Registro de cada control prenatal realizado por el médico.
    Al guardarse, dispara automáticamente la predicción de riesgo IA.
    """
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='controles_paciente',
    )
    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='controles_medico',
    )

    # ── Datos básicos ──────────────────────────────────────────────────────
    fecha             = models.DateField(auto_now_add=True)
    semanas_gestacion = models.IntegerField(verbose_name='Semanas de gestación')
    presion_arterial  = models.CharField(max_length=20, verbose_name='Presión arterial')
    peso              = models.FloatField(verbose_name='Peso (kg)')
    observaciones     = models.TextField(blank=True, default='', verbose_name='Observaciones')

    # ── Datos clínicos para la IA (nuevos) ────────────────────────────────
    altura              = models.FloatField(
        default=1.60, verbose_name='Altura (m)',
        help_text='En metros, ej: 1.62',
    )
    glucosa             = models.FloatField(
        default=90.0, verbose_name='Glucosa (mg/dL)',
        help_text='Glucosa en sangre en mg/dL',
    )
    frecuencia_cardiaca = models.IntegerField(
        default=75, verbose_name='Frecuencia cardíaca (lpm)',
    )
    temperatura         = models.FloatField(
        default=98.0, verbose_name='Temperatura (°F)',
    )
    embarazos_previos   = models.IntegerField(
        default=0, verbose_name='Embarazos previos',
    )
    complicaciones_previas  = models.BooleanField(
        default=False, verbose_name='Complicaciones obstétricas previas',
    )
    diabetes_preexistente   = models.BooleanField(
        default=False, verbose_name='Diabetes preexistente',
    )
    diabetes_gestacional    = models.BooleanField(
        default=False, verbose_name='Diabetes gestacional',
    )

    # ── Campos adicionales del historial físico ───────────────────────────
    proteinuria       = models.CharField(
        max_length=20, blank=True, default='Negativa',
        verbose_name='Proteinuria',
        help_text='Negativa, Trazas, +1, +2, +3',
    )
    diagnostico       = models.TextField(blank=True, default='', verbose_name='Diagnóstico')
    tratamiento       = models.TextField(blank=True, default='', verbose_name='Tratamiento')
    proxima_cita      = models.DateField(null=True, blank=True, verbose_name='Próxima cita')
    examen_fisico     = models.TextField(blank=True, default='', verbose_name='Examen físico')
    resultado_examenes = models.TextField(blank=True, default='', verbose_name='Resultado de exámenes')
    evolucion         = models.TextField(blank=True, default='', verbose_name='Evolución')

    def __str__(self):
        return f"{self.paciente.get_full_name()} — {self.fecha} ({self.semanas_gestacion} sem)"

    @property
    def imc(self) -> float:
        """Calcula el IMC a partir del peso y la altura registrados."""
        if self.altura and self.altura > 0:
            return round(self.peso / (self.altura ** 2), 1)
        return 0.0

    @property
    def presion_sistolica(self) -> int:
        try:
            return int(str(self.presion_arterial).split('/')[0].strip())
        except (IndexError, ValueError):
            return 120

    @property
    def presion_diastolica(self) -> int:
        try:
            return int(str(self.presion_arterial).split('/')[1].strip())
        except (IndexError, ValueError):
            return 80