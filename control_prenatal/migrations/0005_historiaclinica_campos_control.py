from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_prenatal', '0004_add_campos_clinicos_ia'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ── Crear modelo HistoriaClinica ──────────────────────────────────
        migrations.CreateModel(
            name='HistoriaClinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('antecedentes_personales', models.TextField(blank=True, default='', verbose_name='Antecedentes patológicos personales')),
                ('antecedentes_familiares', models.TextField(blank=True, default='', verbose_name='Antecedentes familiares')),
                ('antecedentes_obstetricos', models.TextField(blank=True, default='', verbose_name='Antecedentes obstétricos y ginecológicos')),
                ('gestas', models.IntegerField(default=0, verbose_name='Gestas (G)')),
                ('partos', models.IntegerField(default=0, verbose_name='Partos (P)')),
                ('cesareas', models.IntegerField(default=0, verbose_name='Cesáreas (C)')),
                ('abortos', models.IntegerField(default=0, verbose_name='Abortos (A)')),
                ('hijos_vivos', models.IntegerField(default=0, verbose_name='Hijos vivos (HV)')),
                ('motivo_consulta', models.TextField(blank=True, default='', verbose_name='Motivo de consulta')),
                ('presion_arterial_inicial', models.CharField(blank=True, default='', max_length=20, verbose_name='Presión arterial')),
                ('frecuencia_cardiaca_inicial', models.IntegerField(blank=True, null=True, verbose_name='Frecuencia cardíaca (lpm)')),
                ('frecuencia_respiratoria', models.IntegerField(blank=True, null=True, verbose_name='Frecuencia respiratoria (rpm)')),
                ('temperatura_inicial', models.FloatField(blank=True, null=True, verbose_name='Temperatura (°F)')),
                ('saturacion_oxigeno', models.IntegerField(blank=True, null=True, verbose_name='Saturación de oxígeno (%)')),
                ('estado_conciencia', models.CharField(blank=True, default='Alerta', max_length=50, verbose_name='Estado de conciencia')),
                ('proteinuria', models.CharField(blank=True, default='Negativa', help_text='Negativa / +1 / +2 / +3', max_length=20, verbose_name='Proteinuria')),
                ('peso_inicial', models.FloatField(blank=True, null=True, verbose_name='Peso inicial (kg)')),
                ('talla', models.FloatField(blank=True, null=True, verbose_name='Talla (m)')),
                ('imc_inicial', models.FloatField(blank=True, null=True, verbose_name='IMC preconcepcional')),
                ('examen_fisico', models.TextField(blank=True, default='', verbose_name='Examen físico')),
                ('evolucion_enfermedad', models.TextField(blank=True, default='', verbose_name='Evolución de la enfermedad')),
                ('resultado_examenes', models.TextField(blank=True, default='', verbose_name='Resultado de exámenes complementarios')),
                ('diagnostico', models.TextField(blank=True, default='', verbose_name='Diagnóstico')),
                ('tratamiento', models.TextField(blank=True, default='', verbose_name='Tratamiento')),
                ('paciente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='historia_clinica', to=settings.AUTH_USER_MODEL, verbose_name='Paciente')),
                ('medico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='historias_creadas', to=settings.AUTH_USER_MODEL, verbose_name='Médico que registra')),
            ],
            options={'verbose_name': 'Historia Clínica', 'verbose_name_plural': 'Historias Clínicas'},
        ),
        # ── Agregar campos nuevos a ControlPrenatal ───────────────────────
        migrations.AddField(
            model_name='controlprenatal',
            name='proteinuria',
            field=models.CharField(blank=True, default='Negativa', help_text='Negativa, Trazas, +1, +2, +3', max_length=20, verbose_name='Proteinuria'),
        ),
        migrations.AddField(
            model_name='controlprenatal',
            name='diagnostico',
            field=models.TextField(blank=True, default='', verbose_name='Diagnóstico'),
        ),
        migrations.AddField(
            model_name='controlprenatal',
            name='tratamiento',
            field=models.TextField(blank=True, default='', verbose_name='Tratamiento'),
        ),
        migrations.AddField(
            model_name='controlprenatal',
            name='proxima_cita',
            field=models.DateField(blank=True, null=True, verbose_name='Próxima cita'),
        ),
        migrations.AddField(
            model_name='controlprenatal',
            name='examen_fisico',
            field=models.TextField(blank=True, default='', verbose_name='Examen físico'),
        ),
        migrations.AddField(
            model_name='controlprenatal',
            name='resultado_examenes',
            field=models.TextField(blank=True, default='', verbose_name='Resultado de exámenes'),
        ),
        migrations.AddField(
            model_name='controlprenatal',
            name='evolucion',
            field=models.TextField(blank=True, default='', verbose_name='Evolución'),
        ),
    ]
