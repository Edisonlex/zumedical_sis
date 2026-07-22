"""
Middleware de Auditoría en Tiempo Real
Registra automáticamente todas las acciones del usuario en el sistema
"""
from django.utils.deprecation import MiddlewareMixin
from .models import LogAuditoria
import re


class AuditoriaMiddleware(MiddlewareMixin):
    """
    Middleware que registra automáticamente acciones críticas del usuario.
    Captura operaciones de creación, actualización, eliminación y vistas.
    """
    
    # Rutas excluidas del registro automático (performance)
    EXCLUDED_PATHS = [
        r'^/static/',
        r'^/media/',
        r'^/admin/jsi18n/',
        r'^/favicon\.ico',
        r'^/horas-disponibles/',
        r'^/datos-paciente/',
        r'^/verificar-disponibilidad/',
        r'^/panel/auditoria/data/',
    ]
    
    # Mapeo de URLs a módulos y acciones
    URL_MAPPINGS = {
        # Citas
        r'/agendar-cita/': ('Citas', 'CREATE'),
        r'/citas-medico/': ('Citas', 'VIEW'),
        r'/mis-citas/': ('Citas', 'VIEW'),
        r'/cambiar-estado/\d+/': ('Citas', 'UPDATE'),
        r'/reprogramar/\d+/': ('Citas', 'UPDATE'),
        r'/cancelar-cita': ('Citas', 'CANCELACION'),
        
        # Pacientes
        r'/registrar-paciente/': ('Pacientes', 'CREATE'),
        r'/editar-paciente/': ('Pacientes', 'UPDATE'),
        r'/editar-perfil-paciente/\d+/': ('Pacientes', 'UPDATE'),
        r'/activar-embarazo/\d+/': ('Pacientes', 'UPDATE'),
        r'/desactivar-embarazo/\d+/': ('Pacientes', 'UPDATE'),
        r'/toggle-modulo-prenatal/\d+/': ('Pacientes', 'UPDATE'),
        
        # Controles Prenatales
        r'/registrar-control/': ('Control Prenatal', 'CREATE'),
        r'/historial-prenatal/': ('Control Prenatal', 'VIEW'),
        
        # Historia Clínica
        r'/historia-clinica/crear/': ('Historia Clínica', 'CREATE'),
        r'/historia-clinica/editar/': ('Historia Clínica', 'UPDATE'),
        r'/historia-clinica/ver/': ('Historia Clínica', 'VIEW'),
        
        # Consultas Generales
        r'/consulta-general/registrar/': ('Consulta General', 'CREATE'),
        r'/consulta-general/historial/': ('Consulta General', 'VIEW'),
        r'/consulta-general/ver/\d+/': ('Consulta General', 'VIEW'),
        
        # Programación de Partos
        r'/programar-parto/': ('Programación Parto', 'CREATE'),
        r'/editar-parto/': ('Programación Parto', 'UPDATE'),
        r'/lista-programaciones-parto/': ('Programación Parto', 'VIEW'),
        
        # Admin - Gestión de Usuarios
        r'/panel/usuarios/crear/': ('Usuarios', 'CREATE'),
        r'/panel/usuarios/\d+/editar/': ('Usuarios', 'UPDATE'),
        r'/panel/usuarios/\d+/eliminar/': ('Usuarios', 'DELETE'),
        r'/panel/usuarios/\d+/toggle/': ('Usuarios', 'UPDATE'),
        r'/panel/usuarios/': ('Usuarios', 'VIEW'),
        
        # Admin - Gestión de Médicos
        r'/panel/medicos/crear/': ('Médicos', 'CREATE'),
        r'/panel/medicos/\d+/editar/': ('Médicos', 'UPDATE'),
        r'/panel/medicos/\d+/eliminar/': ('Médicos', 'DELETE'),
        r'/panel/medicos/': ('Médicos', 'VIEW'),
        
        # Admin - Gestión de Pacientes
        r'/panel/pacientes/crear/': ('Pacientes', 'CREATE'),
        r'/panel/pacientes/\d+/editar/': ('Pacientes', 'UPDATE'),
        r'/panel/pacientes/\d+/eliminar/': ('Pacientes', 'DELETE'),
        r'/panel/pacientes/': ('Pacientes', 'VIEW'),
        
        # Admin - Citas y Controles
        r'/panel/citas/\d+/eliminar/': ('Citas', 'DELETE'),
        r'/panel/citas/': ('Citas', 'VIEW'),
        r'/panel/controles/\d+/eliminar/': ('Control Prenatal', 'DELETE'),
        r'/panel/controles/': ('Control Prenatal', 'VIEW'),
    }
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """Se ejecuta antes de procesar la petición"""
        # Guardar método y ruta para process_response
        request._audit_method = request.method
        request._audit_path = request.path
        return None
    
    def process_response(self, request, response):
        """Se ejecuta después de procesar la petición"""
        try:
            # Solo registrar si el usuario está autenticado
            if not request.user.is_authenticated:
                return response
            
            # Excluir rutas estáticas y API
            path = request.path
            for excluded in self.EXCLUDED_PATHS:
                if re.match(excluded, path):
                    return response
            
            # Solo registrar POST (create/update/delete)
            if request.method not in ['POST', 'PUT', 'DELETE']:
                return response
            
            # Solo registrar respuestas exitosas
            if response.status_code not in [200, 201, 302]:
                return response
            
            # Buscar mapeo de URL
            modulo, accion = self._get_module_action(path)
            
            if modulo:
                descripcion = self._build_description(request, modulo, accion, path)
                self._registrar_log(request, accion, modulo, descripcion)
        
        except Exception as e:
            # No romper el flujo por errores de auditoría
            pass
        
        return response
    
    def _get_module_action(self, path):
        """Obtiene el módulo y acción basado en la ruta"""
        for pattern, (modulo, accion) in self.URL_MAPPINGS.items():
            if re.match(pattern, path):
                return modulo, accion
        return None, None
    
    def _build_description(self, request, modulo, accion, path):
        """Construye descripción legible de la acción"""
        user_name = request.user.get_full_name() or request.user.username
        rol = getattr(request.user, 'rol', 'Usuario')
        
        action_text = {
            'CREATE': 'creó',
            'UPDATE': 'actualizó',
            'DELETE': 'eliminó',
            'CANCELACION': 'canceló',
            'VIEW': 'consultó',
        }.get(accion, 'realizó acción en')
        
        return f"{user_name} ({rol}) {action_text} {modulo}"
    
    def _registrar_log(self, request, accion, modulo, descripcion):
        """Registra el log en la base de datos"""
        try:
            LogAuditoria.objects.create(
                usuario=request.user,
                accion=accion,
                modulo=modulo,
                descripcion=descripcion,
                ip_address=self._get_client_ip(request),
                severidad='INFO'
            )
        except Exception:
            pass
    
    def _get_client_ip(self, request):
        """Obtiene la IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
