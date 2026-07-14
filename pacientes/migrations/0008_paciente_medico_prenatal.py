from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0007_paciente_mensaje_prenatal_visto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='medico_prenatal',
            field=models.ForeignKey(
                blank=True,
                help_text='Médico que activó y lleva el seguimiento del embarazo',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='pacientes_prenatales',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Médico prenatal responsable',
            ),
        ),
    ]
