from fastapi import FastAPI
from app.api.routes import router


## Inicialización del microservicio

app = FastAPI(title="Pricing Service")

app.include_router(router, prefix="/pricing", tags=["pricing"])
