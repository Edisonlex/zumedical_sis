from django.db import migrations


def cargar_especialidades(apps, schema_editor):
    Especialidad = apps.get_model('landing', 'Especialidad')

    especialidades = [
        {
            'id': 1,
            'nombre': 'Ginecología y Obstetricia',
            'descripcion': 'Atención integral de la salud femenina, embarazo, parto y puerperio. Seguimiento prenatal, ecografías y control de riesgo obstétrico.',
            'icono': 'fa-baby',
            'tipo': 'prenatal',
            'activo': True,
        },
        {
            'id': 2,
            'nombre': 'Odontología',
            'descripcion': 'Salud bucal completa para toda la familia. Limpieza dental, tratamientos, ortodoncia y cuidado preventivo.',
            'icono': 'fa-tooth',
            'tipo': 'general',
            'activo': True,
        },
        {
            'id': 3,
            'nombre': 'Medicina General',
            'descripcion': 'Consulta médica general para diagnóstico y tratamiento de enfermedades comunes. Atención primaria de salud.',
            'icono': 'fa-stethoscope',
            'tipo': 'general',
            'activo': True,
        },
        {
            'id': 4,
            'nombre': 'Ecografía Diagnóstica',
            'descripcion': 'Diagnóstico por imágenes mediante ultrasonido. Ecografías obstétricas, abdominales y de partes blandas.',
            'icono': 'fa-x-ray',
            'tipo': 'general',
            'activo': True,
        },
        {
            'id': 5,
            'nombre': 'Programación de Partos y Cesáreas',
            'descripcion': 'Planificación y coordinación profesional del nacimiento. Evaluación del bienestar fetal y decisión del tipo de parto.',
            'icono': 'fa-hospital',
            'tipo': 'prenatal',
            'activo': True,
        },
    ]

    for data in especialidades:
        Especialidad.objects.update_or_create(
            id=data['id'],
            defaults={k: v for k, v in data.items() if k != 'id'}
        )


def revertir_especialidades(apps, schema_editor):
    Especialidad = apps.get_model('landing', 'Especialidad')
    Especialidad.objects.filter(id__in=[1, 2, 3, 4, 5]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_especialidades, revertir_especialidades),
    ]
