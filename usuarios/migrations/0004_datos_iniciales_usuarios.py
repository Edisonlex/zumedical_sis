from django.db import migrations
from django.contrib.auth.hashers import make_password


# Contraseña por defecto para todos los usuarios restaurados.
# El admin y cada usuario deben cambiarla tras el primer login.
DEFAULT_PASSWORD = make_password('Zumedical2026!')


def cargar_usuarios(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')

    usuarios = [
        # id, username, first_name, last_name, email, rol, tipo_paciente,
        # is_superuser, is_staff, is_active
        {
            'id': 1,
            'username': 'admin',
            'first_name': '',
            'last_name': '',
            'email': 'edison.zamora9535@utc.edu.ec',
            'rol': 'admin',
            'tipo_paciente': None,
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
        },
        {
            'id': 2,
            'username': 'sulay',
            'first_name': 'Sulay',
            'last_name': 'Baño',
            'email': '',
            'rol': 'paciente',
            'tipo_paciente': 'prenatal',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 3,
            'username': 'Abigail',
            'first_name': 'Abigail',
            'last_name': 'Neira',
            'email': '',
            'rol': 'medico',
            'tipo_paciente': None,
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 4,
            'username': 'Vicenta',
            'first_name': 'Vicenta',
            'last_name': 'Arana',
            'email': '',
            'rol': 'secretaria',
            'tipo_paciente': None,
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 5,
            'username': 'Gloria',
            'first_name': 'Gloria E',
            'last_name': 'Cabrera Arana',
            'email': 'gloria2000c@gmail.com',
            'rol': 'paciente',
            'tipo_paciente': 'prenatal',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 6,
            'username': 'Lizbeth',
            'first_name': 'Lizbeth',
            'last_name': 'Maldonado',
            'email': 'liz2003m@gmail.com',
            'rol': 'paciente',
            'tipo_paciente': 'prenatal',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 8,
            'username': 'Vivi',
            'first_name': 'Viviana',
            'last_name': 'Montece',
            'email': 'viviana.montece123@gmail.com',
            'rol': 'paciente',
            'tipo_paciente': 'prenatal',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 9,
            'username': 'juana26',
            'first_name': 'Juana',
            'last_name': 'Cabrera A',
            'email': 'juana.cabrera52@gmail.com',
            'rol': 'paciente',
            'tipo_paciente': 'general',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 10,
            'username': 'drNayeli',
            'first_name': 'Nayeli',
            'last_name': 'Zambrano',
            'email': 'nayeli.zambrano26@gmail.com',
            'rol': 'medico',
            'tipo_paciente': None,
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
        {
            'id': 11,
            'username': 'belensalguero',
            'first_name': 'Belen',
            'last_name': 'Salguero',
            'email': '09052003salguerod@gmail.com',
            'rol': 'paciente',
            'tipo_paciente': 'prenatal',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
        },
    ]

    for data in usuarios:
        obj, created = Usuario.objects.update_or_create(
            id=data['id'],
            defaults={
                'username': data['username'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'rol': data['rol'],
                'tipo_paciente': data['tipo_paciente'],
                'is_superuser': data['is_superuser'],
                'is_staff': data['is_staff'],
                'is_active': data['is_active'],
                'password': DEFAULT_PASSWORD,
            }
        )


def revertir_usuarios(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    Usuario.objects.filter(id__in=[1, 2, 3, 4, 5, 6, 8, 9, 10, 11]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_logauditoria'),
    ]

    operations = [
        migrations.RunPython(cargar_usuarios, revertir_usuarios),
    ]
