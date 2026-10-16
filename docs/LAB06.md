# Laboratorio 06: Motor de plantillas con Django

**Estudiante:** Sebastián Espíritu Canteño

**Base:** Laboratorio 05, aplicación `movies`. Se conserva su administrador y la página de recomendaciones.

**Desarrollo:** Portal cultural de noticias con Django.

## Ejecución en Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_news
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Abrir http://127.0.0.1:8000/ para ver el portal y `/admin/` para administrar contenido.
`seed_news` crea seis noticias, tres categorías, un autor e imágenes JPEG locales de demostración. Puede repetirse sin sobrescribir noticias existentes. No son noticias periodísticas verificadas.

## Correspondencia con la guía

| Requisito | Implementación |
| --- | --- |
| Aplicación y configuración | `news`, `requirements.txt`, `config/settings.py` |
| Entidades y relaciones | `news/models.py`: Article, Category, Author; autor protegido y categorías N:M |
| Migraciones | `news/migrations/0001_initial.py` |
| Herencia y bloques | `templates/base.html`: title, content, sidebar |
| Fragmento reutilizable | `news/templates/news/_article_card.html`, incluido desde portada y categoría |
| Variables y control | `for`, `empty`, `if` en las plantillas |
| Filtros | `date`, `truncatewords`, `default`, `linebreaksbr` |
| Tres páginas y rutas | `news/urls.py`, enlaces mediante `{% url %}` |
| Estilos y medios | `{% load static %}`, `static/news/site.css`, `MEDIA_ROOT` y rutas de desarrollo |
| Administrador | Columnas, filtros, búsquedas en las tres entidades; slug sugerido y selección múltiple de categorías |
| Datos iniciales | Comando `seed_news`, seis noticias en tres categorías |
| Escapado automático | Noticia `publicar-web-segura` y prueba automatizada de HTML escapado |

Las noticias con fecha futura no se muestran hasta su publicación. Los cambios guardados en el administrador aparecen al recargar el portal. El cuerpo se trata como texto y conserva saltos de línea.

## Escapado automático

Abrir «Aprender a publicar en la web de forma segura». Su cuerpo contiene:

```html
<script>alert("Prueba de escapado")</script>
```

La página muestra la etiqueta literalmente y no dispara una alerta. Django transforma los caracteres especiales en entidades HTML. `linebreaksbr` conserva ese escapado y agrega saltos de línea. No se utiliza `safe` ni se desactiva `autoescape`.

## Casos de prueba

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Las pruebas comprueban herencia y fragmentos, exclusión de noticias futuras, filtrado y categoría vacía, respuestas 404, escapado, actualización real desde el administrador y continuidad de la vista del laboratorio 05.

Verificación manual:

1. Abrir la portada: deben aparecer seis tarjetas con imágenes, autores, fechas y resúmenes.
2. Abrir cada categoría: deben aparecer dos noticias de demostración.
3. Abrir una noticia y navegar a su categoría y de vuelta a la portada.
4. Editar título o cuerpo desde el administrador y recargar la página pública.
5. Revisar la noticia de escapado: etiqueta visible, ninguna alerta.
6. Reducir el ancho de ventana para revisar la distribución móvil.
7. Abrir `/recommendations/` para comprobar la página anterior.

## Evidencias y entrega

Capturar portada, detalle, categoría, administrador, edición reflejada en el portal, prueba de escapado, resultados de pruebas y árbol de archivos en el editor. Adjuntar cada evidencia con nombre del alumno, título, código pertinente, explicación y caso de prueba. Las capturas deben corresponder a la ejecución real.

Repositorio del proyecto: https://github.com/SebastianEspiritu/espiritu-lab05-empresariales. La entrega del documento con capturas y evidencias en el campus se realiza por separado. Las imágenes de noticias se regeneran con `seed_news` y no se versionan.

## Observaciones

Se corrigió la extensión `.htm` de recomendaciones a `.html` para que coincida con su vista. Se conserva la aplicación anterior. La clave local se genera en `.local-secret-key`, ignorada por Git; también puede configurarse con `DJANGO_SECRET_KEY`. El servidor usa configuración de desarrollo y SQLite. El superusuario se crea localmente y su contraseña no forma parte del código.
