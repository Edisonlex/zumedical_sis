from django.urls import path
from . import views

urlpatterns = [
    path('historias/', views.lista_historias, name='lista_historias'),
    path('historias/nueva/', views.crear_historia, name='crear_historia'),
    path('historias/<int:historia_id>/', views.detalle_historia, name='detalle_historia'),
    path('historias/<int:historia_id>/editar/', views.editar_historia, name='editar_historia'),
    
    path('controles/nuevo/', views.crear_control, name='crear_control'),
    path('controles/nuevo/<int:paciente_id>/', views.crear_control, name='crear_control_paciente'),
    path('controles/<int:control_id>/editar/', views.editar_control, name='editar_control'),
    
    path('mi-historial/', views.mi_historial, name='mi_historial'),
]
