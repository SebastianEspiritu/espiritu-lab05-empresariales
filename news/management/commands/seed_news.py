from datetime import timedelta
from io import BytesIO
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageDraw

from news.models import Article, Author, Category


class Command(BaseCommand):
    help = 'Create six demo articles without overwriting existing editorial content.'

    @transaction.atomic
    def handle(self, *args, **options):
        author, _ = Author.objects.get_or_create(
            name='Redacción Espíritu',
            defaults={'biography': 'Un equipo dedicado a explorar el cine, la cultura y las ideas que nos conectan.'},
        )
        sections = [
            ('Cine', 'cine', 'Historias dentro y fuera de la pantalla.'),
            ('Tecnología', 'tecnologia', 'Herramientas e ideas para imaginar el futuro.'),
            ('Cultura', 'cultura', 'Arte, comunidad y nuevas formas de mirar.'),
        ]
        categories = []
        for name, slug, description in sections:
            section, _ = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'description': description},
            )
            categories.append(section)
        stories = [
            ('El cine independiente encuentra nuevas pantallas', 'cine-independiente', 0,
             'Las salas pequeñas y los encuentros vecinales abren un espacio para descubrir otras maneras de contar historias.'),
            ('La tecnología detrás de una buena historia', 'tecnologia-historias', 1,
             'Del guion a la edición, las herramientas digitales acompañan la creatividad sin reemplazar la mirada de quien crea.'),
            ('Una ciudad que se cuenta a través de sus murales', 'ciudad-murales', 2,
             'Recorrer las calles también es leer una memoria colectiva hecha de colores, encuentros y voces del barrio.'),
            ('Volver a los clásicos con una mirada nueva', 'volver-clasicos', 0,
             'Una película cambia cuando cambia quien la mira. Revisitar el archivo puede convertirse en un descubrimiento.'),
            ('Aprender a publicar en la web de forma segura', 'publicar-web-segura', 1,
             'El escapado automático permite mostrar texto aportado por los usuarios sin convertirlo en instrucciones del navegador.'),
            ('Leer juntos para imaginar otros mundos', 'leer-juntos', 2,
             'Los clubes de lectura ofrecen una pausa compartida y una oportunidad para conversar desde experiencias diferentes.'),
        ]
        created_count = 0
        for index, (title, slug, category_index, summary) in enumerate(stories):
            body = (
                f'{summary}\n\nEsta noticia de demostración forma parte del portal cultural Espíritu. '
                'Su contenido se administra desde el panel de Django y se publica sin modificar las plantillas.\n\n'
                'Cada historia invita a observar, compartir preguntas y descubrir nuevas perspectivas. '
                'La relación con su autor y sus categorías permite organizar la información y recorrer el portal.'
            )
            if slug == 'publicar-web-segura':
                body += '\n\nEjemplo de HTML almacenado como texto: <script>alert("Prueba de escapado")</script>\nLa etiqueta debe aparecer literalmente y no ejecutar ninguna alerta.'
            article, created = Article.objects.get_or_create(slug=slug, defaults={
                'title': title, 'summary': summary, 'body': body, 'author': author,
                'published_at': timezone.now() - timedelta(hours=index + 1),
                'image_description': 'Ilustración geométrica editorial creada para esta noticia de demostración.',
            })
            if not created:
                continue
            article.categories.add(categories[category_index])
            palette = [('#ced6be', '#47634c'), ('#ccd7db', '#385968'), ('#e4ccba', '#985e42')]
            background, foreground = palette[category_index]
            image = Image.new('RGB', (960, 600), background)
            draw = ImageDraw.Draw(image)
            rng = random.Random(index)
            for step in range(7):
                x = rng.randint(0, 850)
                y = rng.randint(0, 450)
                draw.rectangle((x, y, x + 120, y + 190), fill=foreground)
            draw.ellipse((280, 100, 680, 500), fill='#f7f5ef')
            draw.ellipse((370, 190, 590, 410), fill=foreground)
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=90)
            article.featured_image.save(f'{slug}.jpg', ContentFile(buffer.getvalue()))
            created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} articles; existing articles preserved.'))
