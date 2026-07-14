
from django.urls import path
from . import views

urlpatterns = [
    path('evaluar-riesgo/', views.evaluar_riesgo, name='evaluar_riesgo'),
    path('ver-predicciones/<int:paciente_id>/', views.ver_predicciones_paciente, name='ver_predicciones_paciente'),
]

