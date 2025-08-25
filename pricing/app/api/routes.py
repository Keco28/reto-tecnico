from fastapi import APIRouter, Depends, status
from app.database.schemas import PricingBase, PricingResponse
from app.api import services


router = APIRouter()

## API de pricing que invoca el servicio de llamado a catálogo

@router.post("/quote", response_model=PricingResponse)
def create_pricing_quote(pricing: PricingBase):
    return services.create_pricing(pricing)

@router.get("/health")
def health_check():
    return {"status": "ok"}