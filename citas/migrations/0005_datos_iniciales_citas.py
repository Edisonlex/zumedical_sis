from django.db import migrations


def cargar_citas(apps, schema_editor):
    Cita = apps.get_model('citas', 'Cita')

    citas = [
        # id, fecha, hora, motivo, estado, medico_id, paciente_id, especialidad_id
        # medico_id aquí son IDs de Usuario (3=Abigail, 10=drNayeli)
        # paciente_id aquí son IDs de Usuario (2=sulay, 5=Gloria, 6=Lizbeth, 8=Vivi, 9=juana26)
        {'id': 1,  'fecha': '2026-03-20', 'hora': '17:00', 'motivo': 'Consulta',             'estado': 'atendido',  'medico_id': 3,  'paciente_id': 2,  'especialidad_id': None},
        {'id': 2,  'fecha': '2026-03-25', 'hora': '00:10', 'motivo': 'control',              'estado': 'atendido',  'medico_id': 3,  'paciente_id': 2,  'especialidad_id': None},
        {'id': 3,  'fecha': '2026-04-24', 'hora': '16:00', 'motivo': 'Examenes',             'estado': 'cancelado', 'medico_id': 3,  'paciente_id': 6,  'especialidad_id': None},
        {'id': 5,  'fecha': '2026-04-24', 'hora': '16:30', 'motivo': 'Seguimiento Rutinario','estado': 'atendido',  'medico_id': 3,  'paciente_id': 6,  'especialidad_id': None},
        {'id': 6,  'fecha': '2026-04-30', 'hora': '14:00', 'motivo': 'Vacunación',           'estado': 'atendido',  'medico_id': 3,  'paciente_id': 6,  'especialidad_id': None},
        {'id': 7,  'fecha': '2026-04-17', 'hora': '12:00', 'motivo': 'Vacunación',           'estado': 'atendido',  'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
        {'id': 8,  'fecha': '2026-04-18', 'hora': '15:30', 'motivo': 'Consulta',             'estado': 'cancelado', 'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
        {'id': 9,  'fecha': '2026-05-29', 'hora': '15:00', 'motivo': 'revision',             'estado': 'atendido',  'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
        {'id': 10, 'fecha': '2026-06-20', 'hora': '14:00', 'motivo': '',                     'estado': 'atendido',  'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 11, 'fecha': '2026-06-25', 'hora': '11:30', 'motivo': 'Prueba',               'estado': 'cancelado', 'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
        {'id': 13, 'fecha': '2026-06-26', 'hora': '11:30', 'motivo': '',                     'estado': 'cancelado', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 19, 'fecha': '2026-07-24', 'hora': '11:30', 'motivo': 'Prueba',               'estado': 'pendiente', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 20, 'fecha': '2026-06-30', 'hora': '14:00', 'motivo': 'diagnos',              'estado': 'cancelada', 'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
        {'id': 21, 'fecha': '2026-07-03', 'hora': '16:00', 'motivo': 'prueb',                'estado': 'cancelada', 'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
        {'id': 22, 'fecha': '2026-06-30', 'hora': '14:30', 'motivo': 'jhhjhk',               'estado': 'cancelada', 'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
        {'id': 23, 'fecha': '2026-06-27', 'hora': '13:00', 'motivo': 'revision',             'estado': 'cancelada', 'medico_id': 3,  'paciente_id': 5,  'especialidad_id': 1},
        {'id': 24, 'fecha': '2026-06-26', 'hora': '10:00', 'motivo': '',                     'estado': 'cancelada', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 25, 'fecha': '2026-06-26', 'hora': '08:30', 'motivo': '',                     'estado': 'cancelada', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 26, 'fecha': '2026-07-02', 'hora': '17:00', 'motivo': '',                     'estado': 'cancelada', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 27, 'fecha': '2026-07-16', 'hora': '14:00', 'motivo': '',                     'estado': 'cancelada', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 28, 'fecha': '2026-07-10', 'hora': '10:00', 'motivo': 'prueba delmotivo',     'estado': 'pendiente', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 29, 'fecha': '2026-07-15', 'hora': '14:00', 'motivo': 'holaaa',               'estado': 'pendiente', 'medico_id': 10, 'paciente_id': 9,  'especialidad_id': 3},
        {'id': 30, 'fecha': '2026-07-02', 'hora': '14:00', 'motivo': 'HOLAAA',               'estado': 'cancelada', 'medico_id': 3,  'paciente_id': 8,  'especialidad_id': None},
    ]

    for data in citas:
        Cita.objects.update_or_create(
            id=data['id'],
            defaults={k: v for k, v in data.items() if k != 'id'}
        )


def revertir_citas(apps, schema_editor):
    Cita = apps.get_model('citas', 'Cita')
    Cita.objects.filter(
        id__in=[1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0004_cita_especialidad'),
        ('usuarios', '0004_datos_iniciales_usuarios'),
        ('landing', '0002_datos_iniciales_especialidades'),
    ]

    operations = [
        migrations.RunPython(cargar_citas, revertir_citas),
    ]
