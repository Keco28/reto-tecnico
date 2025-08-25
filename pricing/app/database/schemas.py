from pydantic import BaseModel, field_validator
import logging
from app.database.tables import TAX_BY_COUNTRY, COUPONS


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Esquemas de los modelos de petición y respuesta

class PricingBase(BaseModel):
    product_sku: str
    coupon: str | None = None
    country: str

    @field_validator("coupon")
    def coupon_valid(cls, v):
        if v not in COUPONS and v is not None:
            logger.error(f"Validation error: coupon '{v}' does not exist")
            raise ValueError(f"coupon '{v}' is not valid")
        return v

    @field_validator("country")
    def country_valid(cls, v):
        if v not in TAX_BY_COUNTRY:
            logger.error(f"Validation error: country '{v}' is not in the list of countries")
            raise ValueError(f"country '{v}' is not valid")
        return v

class PricingResponse(BaseModel):
    product_sku: str
    base_price: float
    final_price: float | None = None 
    currency: str
    total_discounted: float | None = None
    total_taxed: float | None = None