# CocinaFácil - Backend

API REST de CocinaFácil, una aplicación para gestionar y organizar recetas de cocina. Está hecha con Django y Django REST Framework, y la consume el frontend en React.

**Frontend (contraparte):** https://github.com/cristofermartinez7845-blip/cocinafacil-frontend

## Equipo

- Cristopher Francisco Martínez Pérez
- Xóchilt Nicole Rivera Guadrón
- Bryan Miguel Polanco Argueta

Asignatura: Herramientas Avanzadas para el Desarrollo de Aplicaciones (102HAD1), UTLA, Ciclo II-2026.

## Tecnologías

| Tecnología | Uso |
|---|---|
| Django 5.2 | Framework del backend |
| Django REST Framework | API REST |
| django-cors-headers | Permite que el frontend (localhost:5173) consuma la API |
| python-dotenv | Lee las variables de entorno desde el archivo `.env` |
| SQLite | Base de datos en desarrollo |

## Estructura

```
config/       Configuración del proyecto (settings.py, urls.py)
catalogo/     App de datos de referencia: Categoria e Ingrediente
recetas/      App principal: Receta y RecetaIngrediente
```

## Modelo de datos

| Modelo | Descripción |
|---|---|
| `Categoria` | Clasifica las recetas (desayuno, postre, etc.) |
| `Ingrediente` | Catálogo reutilizable de ingredientes |
| `Receta` | Entidad principal. Tiene una `Categoria` (ForeignKey) y un campo `version` |
| `RecetaIngrediente` | Tabla intermedia entre `Receta` e `Ingrediente`: guarda la cantidad y la unidad |

Relaciones: una categoría tiene muchas recetas (ForeignKey), y una receta tiene muchos ingredientes y viceversa (ManyToManyField con `through`).

## Instalación

Requisitos: Python 3.12 o superior.

```powershell
git clone https://github.com/cristofermartinez7845-blip/cocinafacil-backend.git
cd cocinafacil-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Después, abrir el `.env` y poner una `SECRET_KEY` propia entre comillas simples. Se puede generar con:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Preparar la base de datos y arrancar:

```powershell
python manage.py migrate
python manage.py loaddata catalogo_inicial
python manage.py runserver
```

La API queda en `http://127.0.0.1:8000/api/`. El comando `loaddata` carga 4 categorías y 6 ingredientes de ejemplo.

## Variables de entorno

Se configuran en el archivo `.env`, que no se sube a GitHub. Las variables necesarias están listadas en `.env.example`.

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `True` en desarrollo |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por coma |
| `CORS_ALLOWED_ORIGINS` | Orígenes del frontend permitidos, por defecto `http://localhost:5173` |
| `DB_NAME` | Nombre del archivo de la base de datos SQLite |

## Endpoints

| Método | Dirección | Acción |
|---|---|---|
| GET, POST | `/api/categorias/` | Listar y crear categorías |
| GET, PUT, PATCH, DELETE | `/api/categorias/<id>/` | Ver, editar y eliminar una categoría |
| GET, POST | `/api/ingredientes/` | Listar y crear ingredientes |
| GET, PUT, PATCH, DELETE | `/api/ingredientes/<id>/` | Ver, editar y eliminar un ingrediente |
| GET, POST | `/api/recetas/` | Listar y crear recetas |
| GET, PUT, PATCH, DELETE | `/api/recetas/<id>/` | Ver, editar y eliminar una receta |

La lista de recetas admite filtros opcionales: `?categoria=<id>` y `?q=<texto>`.

## Control de concurrencia

Las recetas usan **bloqueo optimista** con el campo `version`. Para editar una receta (PUT o PATCH), el cliente debe enviar la `version` que recibió. Si otra persona la modificó antes, la versión ya no coincide y la API responde **409 Conflict**. Si coincide, se guarda y la versión sube en 1. Además, la actualización usa `select_for_update` dentro de una transacción.

## Validaciones

Los serializers validan que el nombre tenga al menos 3 caracteres, que el tiempo y las porciones sean de 1 o más, que la cantidad de un ingrediente sea mayor que 0, y que no se repita un ingrediente en la misma receta. Las categorías e ingredientes en uso por alguna receta no se pueden eliminar (responde 409).

## Flujo de trabajo en Git

Se usa GitHub Flow:

| Rama | Propósito |
|---|---|
| `main` | Código estable y probado |
| `develop` | Integración de las funcionalidades |
| `feature/<nombre>` | Una rama por tarea, creada desde `develop` |
| `hotfix/<nombre>` | Correcciones urgentes |

Todo cambio llega a `develop` mediante un Pull Request revisado por otro integrante.

| Prefijo de commit | Uso |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de un error |
| `docs:` | Cambios en la documentación |
| `style:` | Formato o diseño, sin cambiar la lógica |
| `refactor:` | Reestructuración sin cambiar el comportamiento |

## Estado del proyecto

| Hito | Estado |
|---|---|
| Sesión 9: apps de Django y modelos | Hecho |
| Sesión 11: API conectada al frontend, con CORS y variables de entorno | Hecho |
| Sesión 13: CRUD completo probado con Postman | En progreso |
| Sesión 14: integración final | Pendiente |

## Cambios de alcance

- (Se completa con fecha y razón cuando se descarte o cambie alguna funcionalidad, como el login o los favoritos.)