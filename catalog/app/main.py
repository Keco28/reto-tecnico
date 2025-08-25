from fastapi import FastAPI
from .api.routes import router
from app.database.db import create_table, drop_table

## Inicialización del microservicio

app = FastAPI(title="Catalog Service")

app.include_router(router, prefix="/products", tags=["products"])
