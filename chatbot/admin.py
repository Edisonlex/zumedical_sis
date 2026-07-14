from django.contrib import admin

from .models import FAQChatbot, InteraccionChatbot


@admin.register(FAQChatbot)
class FAQChatbotAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'pregunta', 'orden', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('pregunta', 'respuesta', 'palabras_clave')
    ordering = ('categoria', 'orden', 'id')
    list_editable = ('orden', 'activo')


@admin.register(InteraccionChatbot)
class InteraccionChatbotAdmin(admin.ModelAdmin):
    list_display = ('canal', 'estado', 'pregunta_relacionada', 'creada_en')
    list_filter = ('canal', 'estado')
    search_fields = ('pregunta', 'respuesta', 'pregunta_relacionada', 'estado')
    readonly_fields = (
        'canal', 'estado', 'pregunta', 'respuesta',
        'pregunta_relacionada', 'direccion_ip', 'creada_en',
    )
    date_hierarchy = 'creada_en'
