# Generated migration for adding CANCELACION action and indexes to LogAuditoria

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_logauditoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logauditoria',
            name='accion',
            field=models.CharField(
                choices=[
                    ('LOGIN', 'Inicio de sesión'),
                    ('LOGOUT', 'Cierre de sesión'),
                    ('CREATE', 'Creación'),
                    ('UPDATE', 'Actualización'),
                    ('DELETE', 'Eliminación'),
                    ('CANCELACION', 'Cancelación'),
                    ('VIEW', 'Visualización'),
                    ('ERROR', 'Error')
                ],
                max_length=20
            ),
        ),
        migrations.AddIndex(
            model_name='logauditoria',
            index=models.Index(fields=['-fecha'], name='usuarios_lo_fecha_idx'),
        ),
        migrations.AddIndex(
            model_name='logauditoria',
            index=models.Index(fields=['usuario', '-fecha'], name='usuarios_lo_usuario_fecha_idx'),
        ),
        migrations.AddIndex(
            model_name='logauditoria',
            index=models.Index(fields=['accion', '-fecha'], name='usuarios_lo_accion_fecha_idx'),
        ),
    ]
