from django.db import migrations


def cargar_pacientes(apps, schema_editor):
    Paciente = apps.get_model('pacientes', 'Paciente')

    pacientes = [
        # Paciente id=1 → usuario_id=2 (sulay)
        {
            'id': 1,
            'usuario_id': 2,
            'cedula': '',
            'edad': None,
            'direccion': '',
            'telefono': '',
            'fecha_ultima_menstruacion': None,
            'fecha_probable_parto': None,
        },
        # Paciente id=2 → usuario_id=5 (Gloria)
        {
            'id': 2,
            'usuario_id': 5,
            'cedula': '0913841748',
            'edad': 37,
            'direccion': 'Balneario Chipe',
            'telefono': '0987654432',
            'fecha_ultima_menstruacion': '2026-04-28',
            'fecha_probable_parto': '2027-02-03',
        },
        # Paciente id=4 → usuario_id=6 (Lizbeth)
        {
            'id': 4,
            'usuario_id': 6,
            'cedula': '1356556776',
            'edad': 21,
            'direccion': 'Quito',
            'telefono': '0987676543',
            'fecha_ultima_menstruacion': '2026-03-03',
            'fecha_probable_parto': '2026-12-10',
        },
        # Paciente id=6 → usuario_id=8 (Vivi)
        {
            'id': 6,
            'usuario_id': 8,
            'cedula': '1323223334',
            'edad': 29,
            'direccion': 'Valencia',
            'telefono': '0944366467',
            'fecha_ultima_menstruacion': '2026-01-15',
            'fecha_probable_parto': '2026-10-22',
        },
        # Paciente id=7 → usuario_id=9 (juana26)
        {
            'id': 7,
            'usuario_id': 9,
            'cedula': '1433245555',
            'edad': None,
            'direccion': '',
            'telefono': '0987332663',
            'fecha_ultima_menstruacion': None,
            'fecha_probable_parto': None,
        },
        # Paciente id=8 → usuario_id=11 (belensalguero)
        {
            'id': 8,
            'usuario_id': 11,
            'cedula': '0502491202',
            'edad': None,
            'direccion': '',
            'telefono': '0969751097',
            'fecha_ultima_menstruacion': None,
            'fecha_probable_parto': None,
        },
    ]

    for data in pacientes:
        Paciente.objects.update_or_create(
            id=data['id'],
            defaults={k: v for k, v in data.items() if k != 'id'}
        )


def revertir_pacientes(apps, schema_editor):
    Paciente = apps.get_model('pacientes', 'Paciente')
    Paciente.objects.filter(id__in=[1, 2, 4, 6, 7, 8]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0003_alter_paciente_cedula_alter_paciente_direccion_and_more'),
        ('usuarios', '0004_datos_iniciales_usuarios'),
    ]

    operations = [
        migrations.RunPython(cargar_pacientes, revertir_pacientes),
    ]
