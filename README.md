## MICROSERVICIO DE CATÁLOGO

Un microservicio basado en FastAPI para la gestión de catálogos de productos, con soporte para SQLAlchemy ORM, SQLite/PostgreSQL y cobertura total de pruebas.

## Características

- Operaciones CRUD para productos (crear, leer, actualizar, eliminar)
- Búsqueda de productos con filtros (categoría, nombre, rango de precios)
- Endpoint /health
- Modelos ORM con SQLAlchemy
- Esquemas de validación con Pydantic
- Sesión de base de datos local
- Reporte y cobertura de pruebas completa con pytest y SQLite en memoria
- Listo para Docker

## Estructura del Proyecto


    app/
        api/
            routes.py         # Endpoints FastAPI
            services.py       # Lógica de negocio
        database/
            db.py             # Sesión, Base y utilidades de BD
            models.py         # Modelo ORM
            schemas.py        # Esquemas Pydantic
    main.py               # Entrada de la app FastAPI

    tests/
        conftest.py         # Configuración y fixtures de pruebas
        test_routes.py      # Pruebas de endpoints API
        test_services.py    # Pruebas de funciones de servicio
        test_schemas.py     # Pruebas de validación de tipos y reglas de negocio

    .dockerignore         # Archivos ignorados por Docker
    .env.example          # Ejemplos de las urls que se van a usar
    compose.yaml          # Definir servicios de Docker
    Dockerfile            # Construcción Docker
    requirements.txt      # Dependencias Python


## Instalación y Ejecución

1. **Crear la base de datos**

	En postgres crearemos una base de datos vacía para almacenar la tabla de productos mas adelante


2. **Configura el entorno e instalar las dependencias**

1. Carpeta catalog 

    crear el entorno virtual de python para la carpeta y activarlo

    [terminal] python -m venv venv
    [terminal] venv\Scripts\Activate.ps1

    luego instalaremos todas las dependencias del proyecto

    [terminal] pip install -r requirements.txt

    finalmente crearemos el archivo `.env` con la url de la base de datos creada en postgres (ejemplo en env.example).

2. Carpeta pricing

    crear el entorno virtual de python para la carpeta y activarlo

    [terminal] python -m venv venv
    [terminal] venv\Scripts\Activate.ps1

    luego instalaremos todas las dependencias del proyecto

    [terminal] pip install -r requirements.txt

     Crear el archivo `.env` con la url de el microservicio de catalogo (ejemplo en env.example).


3. **crear la tabla de productos** 

    **OJO: Solo se hace una vez**

    *terminal desde catalog* ipython
    *terminal especial ipython [1]* from app.database import db, models  
    *terminal especial ipython [2]* db.create_table
    *terminal especial ipython [3]* exit

4. **Ejecuta la aplicación**
	
	*terminal desde catalog* uvicorn app.main:app --reload --port 8000
    *terminal desde pricing* uvicorn app.main:app --reload --port 8001

5. **Documentación Swagger**
	 - Accede a [http://localhost:8000/docs] y [http://localhost:8001/docs] para ver Swagger UI.


## Pruebas

- Ejecuta todas las pruebas:

	*terminal desde catalog o pricing* python -m pytest
	
- Ejecuta pruebas con cobertura:
	
	*terminal desde catalog o pricing* python -m pytest --cov=app --cov-report=term
	
- Ver reporte HTML de cobertura:
	
	*terminal desde catalog o pricing* python -m pytest --cov=app --cov-report=html
	# Abre el archivo htmlcov/index.html en tu navegador
	

## Endpoints

1. catalog

- `GET /products/health` — Verificación de salud
- `POST /products/` — Crear producto
- `GET /products/{sku}` — Obtener producto por SKU
- `GET /products` — Buscar productos (filtros: categoría, nombre, min_price, max_price)
- `PUT /products/{sku}` — Actualizar producto
- `DELETE /products/{sku}` — Eliminar producto

2. Pricing

- `GET /pricing/health` — Verificación de salud
- `POST /pricing/quote` — Crear pricing


## Docker

1. **Construir imagen**
	 ```bash
	 docker build -t catalog-service .
	 ```
2. **Ejecutar contenedor**
	 ```bash
	 docker run -p 8000:8000 --env-file .env catalog-service
	 ```



