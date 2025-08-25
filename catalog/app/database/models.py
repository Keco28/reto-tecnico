from app.database.db import Base
from sqlalchemy import Column, String, Integer, Float


## Modelo base para la creación de la tabla y los productos

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    base_price = Column(Float, index=True, nullable=False)
    currency = Column(String(3), index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
