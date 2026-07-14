from django.db import migrations


def cargar_controles(apps, schema_editor):
    ControlPrenatal = apps.get_model('control_prenatal', 'ControlPrenatal')

    controles = [
        # medico_id y paciente_id son IDs de Usuario
        # medico_id=3 → Abigail; paciente_id=2 → sulay; paciente_id=5 → Gloria
        {
            'id': 1,
            'medico_id': 3,
            'paciente_id': 2,
            'fecha': '2026-03-19',
            'semanas_gestacion': 12,
            'presion_arterial': '110/70',
            'peso': 58.5,
            'observaciones': 'Obs',
        },
        {
            'id': 2,
            'medico_id': 3,
            'paciente_id': 5,
            'fecha': '2026-05-25',
            'semanas_gestacion': 4,
            'presion_arterial': '110/70',
            'peso': 65.5,
            'observaciones': 'Sin novedades',
        },
    ]

    for data in controles:
        # update_or_create no respeta auto_now_add, pero en migraciones
        # los modelos históricos no tienen esa restricción activa.
        ControlPrenatal.objects.update_or_create(
            id=data['id'],
            defaults={k: v for k, v in data.items() if k != 'id'}
        )


def revertir_controles(apps, schema_editor):
    ControlPrenatal = apps.get_model('control_prenatal', 'ControlPrenatal')
    ControlPrenatal.objects.filter(id__in=[1, 2]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('control_prenatal', '0002_initial'),
        ('usuarios', '0004_datos_iniciales_usuarios'),
    ]

    operations = [
        migrations.RunPython(cargar_controles, revertir_controles),
    ]
