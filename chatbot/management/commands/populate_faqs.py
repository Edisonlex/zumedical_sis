from django.core.management.base import BaseCommand
from chatbot.models import FAQChatbot
from ai.knowledge_base import FAQ_CHATBOT, CATEGORIAS_CHATBOT


class Command(BaseCommand):
    help = 'Puebla la base de conocimiento del asistente virtual (102 preguntas en 7 categorías)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los FAQs existentes antes de cargar',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = FAQChatbot.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Se eliminaron {deleted} FAQs existentes'))

        categorias = {c['slug']: c['nombre'] for c in CATEGORIAS_CHATBOT}
        creados = 0
        actualizados = 0

        for idx, faq in enumerate(FAQ_CHATBOT, 1):
            obj, created = FAQChatbot.objects.update_or_create(
                pregunta=faq['pregunta'],
                categoria=faq['categoria'],
                defaults={
                    'respuesta': faq['respuesta'],
                    'palabras_clave': faq.get('palabras_clave', ''),
                    'orden': idx,
                    'activo': True,
                },
            )
            if created:
                creados += 1
            else:
                actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Base de conocimiento cargada exitosamente:'
        ))
        self.stdout.write(f'   Creados  : {creados}')
        self.stdout.write(f'   Actualizados: {actualizados}')
        self.stdout.write(f'   Total FAQs  : {FAQChatbot.objects.count()}')
        self.stdout.write(f'\n📂 Categorías:')
        for slug, nombre in categorias.items():
            count = FAQChatbot.objects.filter(categoria=slug, activo=True).count()
            self.stdout.write(f'   {nombre:<30} {count} preguntas')
