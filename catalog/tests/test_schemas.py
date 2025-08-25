import pytest
from app.database.schemas import ProductCreate, ProductUpdate


def test_valid_product_create():
    product = ProductCreate(
        sku="ABC123",
        name="Test",
        description="desc",
        base_price=1.5,
        currency="COP",
        category="tests"
    )
    assert product.base_price == 1.5

def test_invalid_product_create():
    with pytest.raises(ValueError, match="Field required"):
        ProductCreate(
            sku="ABC123",
            name="Test",
            description="desc",
            base_price=1.5,
            currency="COP"
        )

def test_valid_product_update():
    product = ProductUpdate(
        sku="DEF456",
        category="random"
    )
    
    assert product.sku == "DEF456"
    assert product.base_price is None

def test_invalid_base_price():
    with pytest.raises(ValueError, match="base_price must be greater than 0"):
        ProductCreate(
            sku="sku1",
            name="Test",
            description="desc",
            base_price=0,
            currency="COP",
            category="cat"
        )

def test_invalid_currency():
    with pytest.raises(ValueError, match="currency must be 'COP' or 'USD'"):
        ProductCreate(
            sku="sku1",
            name="Test",
            description="desc",
            base_price=3,
            currency="EUR",
            category="cat"
        )
