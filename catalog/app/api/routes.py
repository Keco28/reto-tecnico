from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.api import services
from app.database import schemas


router = APIRouter()

## APIs de productos que invocan a los servicios

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return services.create_product(db=db, data=product)


@router.get("/{product_sku}", response_model=schemas.Product)
def get_product(product_sku: str, db: Session = Depends(get_db)):
    return services.get_product(db=db, product_sku=product_sku)


@router.get("", response_model=List[schemas.Product])
def search_products(category: str = None, name: str = None, min_price: float = None, max_price: float = None, db: Session = Depends(get_db)):
    return services.search_products(db=db, category=category, name=name, min_price=min_price, max_price=max_price)


@router.put("/{product_sku}", response_model=schemas.Product)
def update_product(product_sku: str, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return services.update_product(db=db, product_sku=product_sku, data=product)


@router.delete("/{product_sku}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_sku: str, db: Session = Depends(get_db)):
    services.delete_product(db=db, product_sku=product_sku)

