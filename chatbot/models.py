from django.db import models


class FAQChatbot(models.Model):
    """
    Base de conocimiento del asistente virtual de Zumedical.
    Organizada por categorías para el flujo guiado del chatbot.
    """
    CATEGORIA_CHOICES = [
        ('centro_medico',       'Centro Médico'),
        ('citas_medicas',       'Citas Médicas'),
        ('controles_prenatales','Controles Prenatales'),
        ('sintomas_alarmas',    'Síntomas y Alarmas'),
        ('nutricion',           'Nutrición y Estilo de Vida'),
        ('uso_sistema',         'Uso del Sistema'),
        ('posparto_lactancia',  'Posparto y Lactancia'),
    ]

    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        default='centro_medico',
        db_index=True,
    )
    pregunta = models.CharField(max_length=300)
    respuesta = models.TextField()
    palabras_clave = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='Separa las palabras clave con comas (uso interno/búsqueda).',
    )
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['categoria', 'orden', 'id']
        verbose_name = 'FAQ Chatbot'
        verbose_name_plural = 'FAQs Chatbot'

    def __str__(self):
        return f'[{self.get_categoria_display()}] {self.pregunta}'


class InteraccionChatbot(models.Model):
    """
    Registro de todas las interacciones del asistente virtual.
    """
    canal = models.CharField(max_length=50, default='landing')
    # Estado o acción que disparó la interacción (inicio, categoria:xxx, faq:123)
    estado = models.CharField(max_length=100, blank=True, default='')
    pregunta = models.TextField()
    respuesta = models.TextField()
    pregunta_relacionada = models.CharField(max_length=300, blank=True, default='')
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creada_en']
        verbose_name = 'Interacción del chatbot'
        verbose_name_plural = 'Interacciones del chatbot'

    def __str__(self):
        return f'{self.canal} | {self.estado} | {self.pregunta[:50]}'
