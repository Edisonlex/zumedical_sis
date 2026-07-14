from django.db import migrations


def cargar_medicos(apps, schema_editor):
    # Usamos SQL directo para evitar conflictos con el estado histórico del modelo
    # (la migración 0001 creó 'especialidad' como CharField, la 0003 agregó 'especialidad_id' como FK)
    db = schema_editor.connection

    medicos = [
        # (id, telefono, usuario_id, especialidad_id)
        (1, '0990130745', 3, 1),   # Abigail → Ginecología y Obstetricia
        (2, '0987767555', 10, 3),  # drNayeli → Medicina General
    ]

    for medico_id, telefono, usuario_id, especialidad_id in medicos:
        existing = db.cursor()
        existing.execute("SELECT id FROM medicos_medico WHERE id = %s", [medico_id])
        if existing.fetchone():
            db.cursor().execute(
                "UPDATE medicos_medico SET telefono=%s, usuario_id=%s, especialidad_id=%s WHERE id=%s",
                [telefono, usuario_id, especialidad_id, medico_id]
            )
        else:
            db.cursor().execute(
                "INSERT INTO medicos_medico (id, telefono, usuario_id, especialidad_id, especialidad) "
                "VALUES (%s, %s, %s, %s, %s)",
                [medico_id, telefono, usuario_id, especialidad_id, '']
            )


def revertir_medicos(apps, schema_editor):
    db = schema_editor.connection
    db.cursor().execute("DELETE FROM medicos_medico WHERE id IN (1, 2)")


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0003_add_especialidad_medico'),
        ('usuarios', '0004_datos_iniciales_usuarios'),
        ('landing', '0002_datos_iniciales_especialidades'),
    ]

    operations = [
        migrations.RunPython(cargar_medicos, revertir_medicos),
    ]
