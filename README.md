# Laboratorio 05: Administrador con Django

**Curso:** Desarrollo de Aplicaciones Empresariales (4-C24-A)  
**Institución:** Tecsup  
**Docente:** Michael Montgomery Rosell  
**Estudiante:** SEBASTIÁN ESPÍRITU CANTEÑO 
**Repositorio GitHub:** `espiritu-lab05-empresariales`

---

## Descripción del Proyecto

Este proyecto es un sistema de gestión cinematográfica desarrollado con **Django**. Permite administrar la información de películas, géneros, actores, directores y calificaciones mediante un panel de administración totalmente personalizado (`/admin/`), e incluye una vista pública orientada a clientes finales para consultar recomendaciones y filtrar películas por género (`/recommendations/`).

---

## Características y Funcionalidades

1. **Modelos ORM Relacionados (`movies/models.py`):**
   - **`Genre`**: Géneros cinematográficos (Acción, Drama, Comedia, Ciencia Ficción, etc.).
   - **`Person`**: Actores y directores con diferenciación de roles (`actor`, `director`, `both`).
   - **`Movie`**: Películas con título, sinopsis, año de estreno, afiche (`ImageField` vía Pillow) y relaciones N:M con géneros y directores.
   - **`Rating`**: Calificaciones numéricas del 1 al 5 (`MinValueValidator`, `MaxValueValidator`) vinculadas mediante `ForeignKey` a las películas.
   - **Auditoría automática:** Todos los modelos incorporan los campos `created_at` y `updated_at`.

2. **Personalización del Django Admin (`movies/admin.py`):**
   - **Inlines (`RatingInline`)**: Permite ingresar y modificar valoraciones directamente desde la pantalla de edición de cada película (`TabularInline`).
   - **Columnas personalizadas (`list_display`)**: Muestra información clave ordenada, incluyendo listas de géneros.
   - **Filtros y Búsqueda (`list_filter`, `search_fields`)**: Búsquedas por título de película y filtrado por año o género.
   - **Protección de Auditoría (`readonly_fields`)**: Bloqueo de edición manual para los timestamps de creación y actualización.

3. **Control de Acceso Basado en Roles (RBAC):**
   - **Superusuario**: Acceso total al panel.
   - **Grupo `editores` (`editor_user`)**: Permisos acotados exclusivamente para agregar y modificar películas (`add_movie`, `change_movie`), restringiendo la posibilidad de eliminar registros (`delete_movie`).

4. **Vista Pública de Recomendaciones (`/recommendations/`):**
   - Agregación dinámica con `Avg('ratings__score')` para calcular el promedio de estrellas por película.
   - Ordenamiento automático de mayor a menor puntuación.
   - Menú interactivo para filtrar por género mediante parámetros `GET`.

---

## Requisitos del Sistema

- **Python:** 3.10 o superior
- **Django:** 5.0+
- **Pillow:** Para soporte de imágenes en `Movie.poster`

---

## Pasos de Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/SebastianEspiritu/espiritu-lab05-empresariales 
   cd espiritu-lab05-empresariales

2. **Crear y activar el entorno virtual:**
   - **En Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **En Linux/macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install django pillow

4. **Ejecutar las migraciones de la base de datos:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Crear Super Usuario:**
   ```bash
   python manage.py createsuperuser
   
6. **Crear Super Usuario:**
   ```bash
   python manage.py runserver


###  Estructura del Proyecto

```text
espiritu-lab05-empresariales/
│
├── config/                  # Configuración global del proyecto Django
│   ├── settings.py          # Apps instaladas, Media URL/Root, Templates
│   ├── urls.py              # Rutas principales del proyecto
│   └── wsgi.py
│
├── movies/                  # Aplicación principal
│   ├── migrations/          # Historial de migraciones de BD
│   ├── templates/
│   │   └── movies/
│   │       └── recommendations.html  # Plantilla HTML de la vista pública
│   ├── admin.py             # Configuración avanzada de ModelAdmin e Inlines
│   ├── models.py            # Modelos Genre, Person, Movie, Rating
│   ├── urls.py              # Rutas internas (/recommendations/)
│   └── views.py             # Lógica con agregación de promedios (Avg)
│
├── media/                   # Archivos multimedia subidos (pósteres)
├── manage.py                # Gestor de comandos Django
├── .gitignore               # Exclusión de venv, db.sqlite3, etc.
└── README.md                # Documentación oficial 
```


### 🌐 Endpoints y Navegación

| Ruta | Descripción | Acceso Requerido |
|---|---|---|
| `http://127.0.0.1:8000/admin/` | Panel de Administración de Django | Usuario Staff / Superusuario |
| `http://127.0.0.1:8000/recommendations/` | Vista Pública de Recomendaciones | Acceso Libre |
