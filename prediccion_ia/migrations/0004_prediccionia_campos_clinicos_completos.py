# Migración manual: agrega los campos clínicos completos al modelo PrediccionIA
# para soportar el motor ML de Random Forest (Fase 10 de la arquitectura IA).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediccion_ia', '0003_prediccionia_puntuacion_riesgo'),
    ]

    operations = [
        # Campos clínicos de entrada (nuevos)
        # NOTA: semanas_gestacion ya existe desde 0001_initial, se omite aquí.
        migrations.AddField(
            model_name='prediccionia',
            name='presion_sistolica',
            field=models.IntegerField(default=0, verbose_name='Presión sistólica'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='presion_diastolica',
            field=models.IntegerField(default=0, verbose_name='Presión diastólica'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='altura',
            field=models.FloatField(default=1.60, verbose_name='Altura (m)'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='imc',
            field=models.FloatField(default=0.0, verbose_name='IMC'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='frecuencia_cardiaca',
            field=models.IntegerField(default=75, verbose_name='Frecuencia cardíaca'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='temperatura',
            field=models.FloatField(default=98.0, verbose_name='Temperatura (°F)'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='embarazos_previos',
            field=models.IntegerField(default=0, verbose_name='Embarazos previos'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='complicaciones_previas',
            field=models.BooleanField(default=False, verbose_name='Complicaciones previas'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='diabetes_preexistente',
            field=models.BooleanField(default=False, verbose_name='Diabetes preexistente'),
        ),
        migrations.AddField(
            model_name='prediccionia',
            name='diabetes_gestacional',
            field=models.BooleanField(default=False, verbose_name='Diabetes gestacional'),
        ),

        # Actualizar verbose_name del campo nivel_riesgo y agregar choices
        migrations.AlterField(
            model_name='prediccionia',
            name='nivel_riesgo',
            field=models.CharField(
                choices=[('Bajo', '🟢 Bajo'), ('Medio', '🟡 Medio'), ('Alto', '🔴 Alto')],
                max_length=10,
                verbose_name='Nivel de riesgo',
            ),
        ),
        migrations.AlterField(
            model_name='prediccionia',
            name='puntuacion_riesgo',
            field=models.IntegerField(default=0, verbose_name='Probabilidad (%)'),
        ),
    ]
