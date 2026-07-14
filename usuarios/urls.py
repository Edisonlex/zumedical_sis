from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('medico-dashboard/', views.medico_dashboard, name='medico_dashboard'),
    path('secretaria-dashboard/', views.secretaria_dashboard, name='secretaria_dashboard'),
    
    #PACIENTE
    path('paciente-dashboard/', views.paciente_dashboard, name='paciente_dashboard'),
    path('registro/', views.registro_paciente, name='registro'),
    path('verificar-disponibilidad/', views.verificar_disponibilidad, name='verificar_disponibilidad'),
    path('agendar-cita/', views.agendar_cita, name='agendar_cita'),
    path('mis-citas/', views.ver_citas, name='ver_citas'),
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),

    path('citas-medico/', views.citas_medico, name='citas_medico'),
    path('cambiar-estado/<int:cita_id>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
    path('pacientes-medico/', views.pacientes_medico, name='pacientes_medico'),
    path('activar-embarazo/<int:paciente_id>/', views.activar_embarazo, name='activar_embarazo'),
    path('registrar-control/', views.registrar_control, name='registrar_control'),
    path('historial-prenatal/', views.historial_prenatal, name='historial_prenatal'),
    path('editar-paciente/<int:paciente_id>/', views.editar_perfil_paciente, name='editar_perfil_paciente'),
    path('mi-perfil-medico/', views.perfil_medico, name='perfil_medico'),
    
    # Historia Clínica Obstétrica (prenatal)
    path('historia-clinica/crear/<int:paciente_id>/', views.crear_historia_clinica, name='crear_historia_clinica'),
    path('historia-clinica/ver/<int:paciente_id>/', views.ver_historia_clinica, name='ver_historia_clinica'),
    path('historia-clinica/editar/<int:historia_id>/', views.editar_historia_clinica, name='editar_historia_clinica'),

    # Consulta General (médico general)
    path('consulta-general/registrar/', views.registrar_consulta_general, name='registrar_consulta_general'),
    path('consulta-general/historial/', views.historial_consultas_generales, name='historial_consultas_generales'),
    path('consulta-general/ver/<int:consulta_id>/', views.ver_consulta_general, name='ver_consulta_general'),

    # Programación de Partos (médico prenatal → paciente prenatal)
    path('programar-parto/', views.programar_parto, name='programar_parto'),
    path('programar-parto/<int:parto_id>/editar/', views.editar_parto, name='editar_parto'),
    path('programaciones-parto/', views.lista_programaciones_parto, name='lista_programaciones_parto'),
    
    #SECRETARIA
    path('registrar-paciente/', views.registrar_paciente, name='registrar_paciente'),
    path('editar-paciente-secretaria/<int:paciente_id>/', views.editar_paciente_secretaria, name='editar_paciente_secretaria'),
    path('agendar-cita-secretaria/', views.agendar_cita_secretaria, name='agendar_cita_secretaria'),
    path('reprogramar/<int:cita_id>/', views.reprogramar_cita, name='reprogramar_cita'),
    path('citas-secretaria/', views.citas_secretaria, name='citas_secretaria'),
    path('horas-disponibles/', views.obtener_horas_disponibles, name='horas_disponibles'),
    path('datos-paciente/', views.datos_paciente, name='datos_paciente'),
    path('buscar-pacientes/', views.buscar_pacientes, name='buscar_pacientes'),
    path('mi-perfil-secretaria/', views.perfil_secretaria, name='perfil_secretaria'),
    path('secretaria/pacientes/', views.lista_pacientes_secretaria, name='lista_pacientes_secretaria'),
    path('secretaria/registrar/<str:tipo>/', views.registrar_paciente, name='registrar_paciente'),
    path('secretaria/toggle-prenatal/<int:paciente_id>/', views.toggle_modulo_prenatal, name='toggle_modulo_prenatal'),

    #ADMIN
    path('panel/usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('panel/medicos/', views.lista_medicos, name='lista_medicos'),
    path('panel/pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('panel/citas/', views.todas_citas, name='todas_citas'),
    path('panel/controles/', views.controles_admin, name='controles_admin'),
    path('panel/pacientes/crear-general/', views.admin_crear_paciente_general, name='admin_crear_paciente_general'),

    # ADMIN — CRUD completo
    path('panel/usuarios/crear/', views.admin_crear_usuario, name='admin_crear_usuario'),
    path('panel/usuarios/<int:usuario_id>/editar/', views.admin_editar_usuario, name='admin_editar_usuario'),
    path('panel/usuarios/<int:usuario_id>/eliminar/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    path('panel/medicos/crear/', views.admin_crear_medico, name='admin_crear_medico'),
    path('panel/medicos/<int:medico_id>/editar/', views.admin_editar_medico, name='admin_editar_medico'),
    path('panel/medicos/<int:medico_id>/eliminar/', views.admin_eliminar_medico, name='admin_eliminar_medico'),
    path('panel/pacientes/crear/', views.admin_crear_paciente, name='admin_crear_paciente'),
    path('panel/pacientes/<int:paciente_id>/editar/', views.admin_editar_paciente, name='admin_editar_paciente'),
    path('panel/pacientes/<int:paciente_id>/eliminar/', views.admin_eliminar_paciente, name='admin_eliminar_paciente'),
    path('panel/citas/<int:cita_id>/eliminar/', views.admin_eliminar_cita, name='admin_eliminar_cita'),
    path('panel/controles/<int:control_id>/eliminar/', views.admin_eliminar_control, name='admin_eliminar_control'),

    path('panel/usuarios/<int:usuario_id>/toggle/', views.toggle_usuario, name='toggle_usuario'),

    path('panel/auditoria/', views.auditoria_admin, name='auditoria_admin'),
    path('panel/auditoria/data/', views.auditoria_admin_data, name='auditoria_admin_data'),
    path('auditoria/config/', views.auditoria_config, name='auditoria_config'),
    path('auditoria/limpiar/', views.auditoria_limpiar, name='auditoria_limpiar'),

    # REPORTES
    path('reportes/pacientes/', views.reporte_pacientes_data, name='reporte_pacientes_data'),
    path('reportes/medicos/',   views.reporte_medicos_data,   name='reporte_medicos_data'),
    path('reportes/citas/',     views.reporte_citas_data,     name='reporte_citas_data'),
    path('reportes/controles/', views.reporte_controles_data, name='reporte_controles_data'),
    path('reportes/usuarios/',  views.reporte_usuarios_data,  name='reporte_usuarios_data'),
]