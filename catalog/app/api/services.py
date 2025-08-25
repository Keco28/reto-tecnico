import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database import models, schemas


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Funciones CRUD para los productos

## CREATE
def create_product(db: Session, data: schemas.ProductCreate):
    logger.info(f"Attempting to create product with SKU: {data.sku}")
    existing_product = db.query(models.Product).filter(models.Product.sku == data.sku).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    product_instance = models.Product(**data.model_dump())
    db.add(product_instance)
    db.commit()
    db.refresh(product_instance)
    return product_instance

## READ
def get_product(db: Session, product_sku: str):
    logger.info(f"Fetching product with SKU: {product_sku}")
    existing_product = db.query(models.Product).filter(models.Product.sku == product_sku).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return existing_product

def search_products(db: Session, category: str = None, name: str = None, min_price: float = None, max_price: float = None):
    logger.info(f"Searching products with filters - Category: {category}, Name: {name}, Min Price: {min_price}, Max Price: {max_price}")
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))
    if min_price:
        query = query.filter(models.Product.base_price >= min_price)
    if max_price:
        query = query.filter(models.Product.base_price <= max_price)
    count = query.count()
    if not count:
        raise HTTPException(status_code=404, detail="No products found")
    return query.all()

## UPDATE
def update_product(db: Session, product_sku: str, data: schemas.ProductUpdate):
    logger.info(f"Updating product with SKU: {product_sku}")
    product_instance = db.query(models.Product).filter(models.Product.sku == product_sku).first()
    if not product_instance:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in data.model_dump().items():
        setattr(product_instance, key, value if value is not None else getattr(product_instance, key))
    db.commit()
    db.refresh(product_instance)
    return product_instance

## DELETE
def delete_product(db: Session, product_sku: str):
    logger.info(f"Deleting product with SKU: {product_sku}")
    product_instance = db.query(models.Product).filter(models.Product.sku == product_sku).first()
    if not product_instance:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product_instance)
    db.commit()