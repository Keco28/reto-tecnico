from pydantic import BaseModel, field_validator, ConfigDict
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Esquemas base de los productos para su validación y tratamiento

class ProductBase(BaseModel):
    sku: str
    name: str
    description: str
    base_price: float
    currency: str
    category: str
    
    @field_validator("base_price")
    def price_positive(cls, v):
        if v <= 0:
            logger.error(f"Validation error: base_price must be greater than 0") 
            raise ValueError("base_price must be greater than 0")
        return v

    @field_validator("currency")
    def currency_valid(cls, v):
        if v not in ("COP", "USD"):
            logger.error(f"Validation error: currency must be 'COP' or 'USD'")
            raise ValueError("currency must be 'COP' or 'USD'")
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    sku: str | None = None
    name: str | None = None
    description: str | None = None
    base_price: float | None = None
    currency: str | None = None
    category: str | None = None

class Product(ProductBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
