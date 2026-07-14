from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0002_initial'),
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='especialidad',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='landing.especialidad'
            ),
        ),
    ]