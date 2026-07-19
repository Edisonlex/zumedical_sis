from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, timedelta
import json
from .models import ControlPrenatal, HistoriaClinica

User = get_user_model()


class EditarControlPrenatalTest(TestCase):
    """Test suite para el endpoint de edición de controles prenatales (editar_control_prenatal)."""

    def setUp(self):
        """Configurar usuarios de prueba y controles prenatales."""
        self.client = Client()
        
        # Crear usuario médico
        self.medico = User.objects.create_user(
            username='medico_test',
            password='pass123456',
            email='medico@test.com',
            rol='medico'
        )
        
        # Crear usuario admin
        self.admin = User.objects.create_user(
            username='admin_test',
            password='pass123456',
            email='admin@test.com',
            rol='admin'
        )
        
        # Crear usuario paciente
        self.paciente = User.objects.create_user(
            username='paciente_test',
            password='pass123456',
            email='paciente@test.com',
            rol='paciente',
            genero='femenino'
        )
        
        # Crear historia clínica para el paciente
        self.historia = HistoriaClinica.objects.create(
            paciente=self.paciente,
            medico=self.medico,
            peso_inicial=65.0,
            talla=1.62,
        )
        
        # Crear control prenatal de prueba
        self.control = ControlPrenatal.objects.create(
            paciente=self.paciente,
            medico=self.medico,
            semanas_gestacion=20,
            presion_arterial='120/80',
            peso=68.0,
            altura=1.62,
            glucosa=95.0,
            frecuencia_cardiaca=75,
            temperatura=98.6,
            embarazos_previos=1,
            diagnostico='Control prenatal normal',
            tratamiento='Vitaminas prenatales',
            observaciones='Todo normal',
            proxima_cita=date.today() + timedelta(weeks=4),
        )
        
        self.url = reverse('api_editar_control', kwargs={'control_id': self.control.id})

    def test_get_control_prenatal_authenticated_medico(self):
        """Test: GET devuelve datos del control para médico autenticado."""
        self.client.login(username='medico_test', password='pass123456')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], self.control.id)
        self.assertEqual(data['data']['semanas_gestacion'], 20)
        self.assertEqual(data['data']['presion_arterial'], '120/80')
        self.assertEqual(data['data']['peso'], 68.0)
        self.assertEqual(data['data']['glucosa'], 95.0)

    def test_get_control_prenatal_authenticated_admin(self):
        """Test: GET devuelve datos del control para admin autenticado."""
        self.client.login(username='admin_test', password='pass123456')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], self.control.id)

    def test_get_control_prenatal_no_authentication(self):
        """Test: GET rechaza acceso sin autenticación (redirect login)."""
        response = self.client.get(self.url)
        # Django redirige a login cuando no está autenticado
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login') or response.url.startswith('/login'))

    def test_get_control_prenatal_paciente_access_denied(self):
        """Test: GET rechaza acceso a paciente (no médico/admin)."""
        self.client.login(username='paciente_test', password='pass123456')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('permisos', data['error'].lower())

    def test_post_edit_control_valid_data_medico(self):
        """Test: POST actualiza control con datos válidos (médico)."""
        self.client.login(username='medico_test', password='pass123456')
        
        updated_data = {
            'paciente': self.paciente.id,
            'semanas_gestacion': 24,
            'presion_arterial': '118/78',
            'peso': 70.0,
            'altura': 1.62,
            'glucosa': 98.0,
            'frecuencia_cardiaca': 72,
            'temperatura': 98.4,
            'embarazos_previos': 1,
            'diagnostico': 'Control prenatal normal - 24 semanas',
            'tratamiento': 'Vitaminas prenatales + calcio',
            'observaciones': 'Presión estable',
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Verificar que el control se actualizó en la BD
        self.control.refresh_from_db()
        self.assertEqual(self.control.semanas_gestacion, 24)
        self.assertEqual(self.control.presion_arterial, '118/78')
        self.assertEqual(self.control.peso, 70.0)
        self.assertEqual(self.control.glucosa, 98.0)

    def test_post_edit_control_valid_data_admin(self):
        """Test: POST actualiza control con datos válidos (admin)."""
        self.client.login(username='admin_test', password='pass123456')
        
        updated_data = {
            'paciente': self.paciente.id,
            'semanas_gestacion': 28,
            'presion_arterial': '122/82',
            'peso': 72.0,
            'altura': 1.62,
            'glucosa': 100.0,
            'frecuencia_cardiaca': 76,
            'temperatura': 98.5,
            'embarazos_previos': 1,
            'diagnostico': 'Control prenatal - 28 semanas',
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        self.control.refresh_from_db()
        self.assertEqual(self.control.semanas_gestacion, 28)

    def test_post_edit_control_paciente_access_denied(self):
        """Test: POST rechaza acceso a paciente (no médico/admin)."""
        self.client.login(username='paciente_test', password='pass123456')
        
        updated_data = {
            'semanas_gestacion': 30,
            'presion_arterial': '120/80',
            'peso': 75.0,
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_post_edit_control_invalid_json(self):
        """Test: POST rechaza JSON inválido."""
        self.client.login(username='medico_test', password='pass123456')
        
        response = self.client.post(
            self.url,
            data='{"invalid json}',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('inválidos', data['error'].lower())

    def test_post_edit_control_missing_required_field(self):
        """Test: POST rechaza datos incompletos (campo requerido faltante)."""
        self.client.login(username='medico_test', password='pass123456')
        
        updated_data = {
            'paciente': self.paciente.id,
            'presion_arterial': '120/80',
            # Falta semanas_gestacion que es requerido
            'peso': 70.0,
            'altura': 1.62,
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('error', data.keys())
        self.assertIn('errors', data.keys())

    def test_post_edit_control_invalid_semanas_gestacion(self):
        """Test: POST rechaza valor inválido para semanas_gestacion."""
        self.client.login(username='medico_test', password='pass123456')
        
        updated_data = {
            'paciente': self.paciente.id,
            'semanas_gestacion': 'invalid',  # No es número
            'presion_arterial': '120/80',
            'peso': 70.0,
            'altura': 1.62,
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_post_edit_control_invalid_peso(self):
        """Test: POST rechaza valor inválido para peso."""
        self.client.login(username='medico_test', password='pass123456')
        
        updated_data = {
            'paciente': self.paciente.id,
            'semanas_gestacion': 24,
            'presion_arterial': '120/80',
            'peso': 'invalid',  # No es número
            'altura': 1.62,
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_post_edit_control_nonexistent_control(self):
        """Test: GET/POST retorna 404 para control inexistente."""
        self.client.login(username='medico_test', password='pass123456')
        
        fake_url = reverse('api_editar_control', kwargs={'control_id': 9999})
        response = self.client.get(fake_url)
        
        self.assertEqual(response.status_code, 404)

    def test_post_edit_control_partial_update(self):
        """Test: POST puede actualizar solo algunos campos."""
        self.client.login(username='medico_test', password='pass123456')
        
        original_diagnostico = self.control.diagnostico
        
        updated_data = {
            'paciente': self.paciente.id,
            'semanas_gestacion': 20,
            'presion_arterial': '115/75',  # Solo cambiar presión
            'peso': 68.0,
            'altura': 1.62,
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.control.refresh_from_db()
        self.assertEqual(self.control.presion_arterial, '115/75')
        # El diagnóstico original debe mantenerse si no se modifica
        self.assertEqual(self.control.diagnostico, original_diagnostico)

    def test_post_edit_control_preserves_creation_date(self):
        """Test: Editar control no cambia la fecha de creación."""
        self.client.login(username='medico_test', password='pass123456')
        
        original_fecha = self.control.fecha
        
        updated_data = {
            'paciente': self.paciente.id,
            'semanas_gestacion': 24,
            'presion_arterial': '120/80',
            'peso': 70.0,
            'altura': 1.62,
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.control.refresh_from_db()
        # Verificar que la fecha no cambió
        self.assertEqual(self.control.fecha, original_fecha)

    def test_get_control_returns_all_fields(self):
        """Test: GET retorna todos los campos del control."""
        self.client.login(username='medico_test', password='pass123456')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Verificar que contiene todos los campos importantes
        required_fields = [
            'id', 'fecha', 'semanas_gestacion', 'presion_arterial',
            'glucosa', 'peso', 'altura', 'frecuencia_cardiaca',
            'temperatura', 'diagnostico', 'tratamiento', 'observaciones',
            'proxima_cita', 'examen_fisico', 'resultado_examenes',
            'evolucion', 'proteinuria'
        ]
        
        for field in required_fields:
            self.assertIn(field, data['data'])

    def test_post_edit_control_with_empty_optional_fields(self):
        """Test: POST puede dejar campos opcionales vacíos."""
        self.client.login(username='medico_test', password='pass123456')
        
        updated_data = {
            'paciente': self.paciente.id,
            'semanas_gestacion': 24,
            'presion_arterial': '120/80',
            'peso': 70.0,
            'altura': 1.62,
            'diagnostico': '',  # Campo opcional, dejarlo vacío
            'tratamiento': '',  # Campo opcional, dejarlo vacío
            'observaciones': '',  # Campo opcional, dejarlo vacío
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
