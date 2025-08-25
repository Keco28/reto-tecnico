## MICROSERVICIO DE CATÁLOGO


# Características


- Operaciones CRUD para productos (crear, leer, actualizar, eliminar)
- Búsqueda de productos con filtros (categoría, nombre, rango de precios)
- Endpoint /health
- Modelos ORM con SQLAlchemy
- Esquemas de validación con Pydantic
- Sesión de base de datos local
- Reporte y cobertura de pruebas completa con pytest y SQLite en memoria
- Listo para Docker


## MICROSERVICIO DE PRICING


# Características


- Creación de pricing con llamado a la API de catálogo
- Endpoint /health
- Esquemas de validación con Pydantic
- Tablas de datos en local
- Reporte y cobertura de pruebas completa con pytest e integración con catálogo
- Listo para Docker


## Estructura del Proyecto


catalog/
    app/
        api/
            routes.py         # Endpoints FastAPI
            services.py       # Lógica de negocio
        database/
            db.py             # Sesión, Base y utilidades de BD
            models.py         # Modelo ORM
            schemas.py        # Esquemas Pydantic


    tests/
        conftest.py         # Configuración y fixtures de pruebas
        test_routes.py      # Pruebas de endpoints API
        test_services.py    # Pruebas de funciones de servicio
        test_schemas.py     # Pruebas de validación de tipos y reglas de negocio


    main.py               # Entrada de la app FastAPI
    .dockerignore         # Archivos ignorados por Docker
    .env.example          # Ejemplos de las urls que se van a usar
    compose.yaml          # Definir servicios de Docker
    Dockerfile            # Construcción Docker
    requirements.txt      # Dependencias Python


pricing
    app/
        api/
            routes.py         # Endpoints FastAPI
            services.py       # Lógica de negocio
        database/
            tables.py         # Tablas de prueba
            schemas.py        # Esquemas Pydantic


    tests/
        test_routes.py      # Pruebas de endpoints de la API de catálogo
        test_services.py    # Pruebas de funcion de servicio
        test_schemas.py     # Pruebas de validación de tipos y reglas de negocio


    main.py               # Entrada de la app FastAPI
    .dockerignore         # Archivos ignorados por Docker
    .env.example          # Ejemplos de las urls que se van a usar
    compose.yaml          # Definir servicios de Docker
    Dockerfile            # Construcción Docker
    requirements.txt      # Dependencias Python
.gitignore         # Archivos ignorados por Git




## Instalación y Ejecución


1. **Clonar repo y preparar entorno**


    - Clonamos el repositorio desde la ruta https://github.com/Keco28/reto-tecnico
    - Creamos un archivo .env en la carpeta catalog y uno en la de pricing (siguiendo el ejemplo de su respectivo .env.example)




2. **Docker**


    Para iniciar docker en cada microservicio, haremos los siguiente:
   
    # **Crear red compartida**:


        En una terminal cualquiera escribiremos el siguiente comando


            docker network create shared_network


    # **Levantar servidores**


        Para levantar los servidores de catalog y pricing abriremos 2 terminales y accederemos a las carpetas de los servicios
        - #1[reto-tecnico>] cd catalog
        - #2[reto-tecnico>] cd pricing


        Luego ejecutaremos el siguiente comando en ambas terminales


            docker compose up --build


    # **Crear tabla de base de datos**


        Para crear la tabla que usara el servicio de catalogo abrimos una nueva terminal y copiamos los siguientes comandos en orden


        **OJO: Solo se hace una vez**


            docker exec -it catalog-server-1 bash  (para acceder a la terminal del contenedor)
            ipython
        [1] from app.database import db, models
        [2] db.create_table()


3. **Preparación de datos iniciales de la tabla y prueba de endpoints**


    Para probar los endpoints accedemos a la documentación de Swagger:
    - [http://localhost:8000/docs] y [http://localhost:8001/docs]


    Crearemos un registro inicial para los tests de integración mas adelante


    Seleccionando el endpoint POST /products/ Create Product o en [http://localhost:8000/docs#/products/create_product_products__post]
    Presionamos en el botón de [Try it out] y en el request body del endpoint pasaremos estos valores


        {
            "sku": "ABC123",
            "name": "test",
            "description": "desc",
            "base_price": 100,
            "currency": "USD",
            "category": "categ"
        }


    A partir de esto se pueden probar libremente los endpoints desde la documentación de Swagger o por metodo curl si asi se desea


    Ejemplos curl:


        catalog:


            Endpoint GET /productS/{product_skuS} ==> curl -X GET "http://localhost:8000/products/ABC123" -H "accept: application/json"


            Endpoint POST /products/ ==> curl -X POST http://localhost:8000/products/ -H "Accept: application/json" -H "Content-Type: application/json" -d "{\"sku\": \"DEF456\", \"name\": \"nombre\", \"description\": \"descripcion\", \"base_price\": 200, \"currency\": \"COP\", \"category\": \"categoria\"}"


        pricing:


            Endpoint POST /pricing/quote ==> curl -X POST http://localhost:8001/pricing/quote -H "Accept: application/json" -H "Content-Type: application/json" -d "{\"product_sku\": \"ABC123\", \"coupon\": \"BANCOLMARTES\", \"country\": \"CO\"}"


## Pruebas


- Para ejecutar las pruebas de cada servidor abriremos 2 terminales y accederemos a las carpetas de los contenedores
        - #1[reto-tecnico>] docker exec -it catalog-server-1 bash
        - #2[reto-tecnico>] docker exec -it pricing-server-1 bash


- Ejecuta todas las pruebas:


    desde ambas terminales para correr sus respectivos tests:
        python -m pytest
   
- Ejecuta pruebas con cobertura:
   
    desde ambas terminales para ver la cobertura de los tests:
        python -m pytest --cov=app --cov-report=term
   
- Ver reporte HTML de cobertura:
   
    desde ambas terminales para ver el reporte de cobertura html:
        python -m pytest --cov=app --cov-report=html


    **OJO**
    # Para ver este reporte tendremos que acceder a los archivos del contenedor en docker y descargar la carpeta app/htmlcov para cada servicio
    # Luego de descargar la carpeta se abre el archivo index.html donde se encuentra el reporte
   