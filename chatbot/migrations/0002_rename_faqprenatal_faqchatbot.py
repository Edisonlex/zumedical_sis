"""
Migración 0002:
- Renombra FAQPrenatal → FAQChatbot
- Agrega campo 'categoria' con default 'centro_medico'
- Agrega campo 'estado' a InteraccionChatbot
- Amplía max_length de pregunta y pregunta_relacionada
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        # 1. Renombrar tabla FAQPrenatal → FAQChatbot
        migrations.RenameModel(
            old_name='FAQPrenatal',
            new_name='FAQChatbot',
        ),

        # 2. Agregar campo categoria a FAQChatbot
        migrations.AddField(
            model_name='faqchatbot',
            name='categoria',
            field=models.CharField(
                choices=[
                    ('centro_medico',       'Centro Médico'),
                    ('citas_medicas',       'Citas Médicas'),
                    ('controles_prenatales','Controles Prenatales'),
                    ('sintomas_alarmas',    'Síntomas y Alarmas'),
                    ('nutricion',           'Nutrición y Estilo de Vida'),
                    ('uso_sistema',         'Uso del Sistema'),
                    ('posparto_lactancia',  'Posparto y Lactancia'),
                ],
                db_index=True,
                default='centro_medico',
                max_length=50,
            ),
        ),

        # 3. Ampliar max_length de pregunta en FAQChatbot (200 → 300)
        migrations.AlterField(
            model_name='faqchatbot',
            name='pregunta',
            field=models.CharField(max_length=300),
        ),

        # 4. Actualizar Meta.ordering y verbose_name de FAQChatbot
        migrations.AlterModelOptions(
            name='faqchatbot',
            options={
                'ordering': ['categoria', 'orden', 'id'],
                'verbose_name': 'FAQ Chatbot',
                'verbose_name_plural': 'FAQs Chatbot',
            },
        ),

        # 5. Agregar campo estado a InteraccionChatbot
        migrations.AddField(
            model_name='interaccionchatbot',
            name='estado',
            field=models.CharField(blank=True, default='', max_length=100),
        ),

        # 6. Ampliar max_length de pregunta_relacionada (200 → 300)
        migrations.AlterField(
            model_name='interaccionchatbot',
            name='pregunta_relacionada',
            field=models.CharField(blank=True, default='', max_length=300),
        ),

        # 7. Actualizar verbose_name de InteraccionChatbot
        migrations.AlterModelOptions(
            name='interaccionchatbot',
            options={
                'ordering': ['-creada_en'],
                'verbose_name': 'Interacción del chatbot',
                'verbose_name_plural': 'Interacciones del chatbot',
            },
        ),
    ]
