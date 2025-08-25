import pytest
from app.api.services import create_product, get_product, search_products, update_product, delete_product
from app.database import schemas

##Setup de el ambiente de pruebas

def test_create_product(db, new_product):
    product = create_product(db, new_product)
    assert product.sku == "serv123"
    assert product.name == "serv"

def test_invalid_create_product(db, existing_product):
    with pytest.raises(Exception):
        create_product(db, existing_product)

def test_invalid_create_missing_product(db):
    with pytest.raises(Exception):
        create_product(db, schemas.ProductCreate(
            sku="serv123",
            base_price=40,
            currency="USD"
        ))

def test_get_product(db):
    product = get_product(db, "ABC123")
    assert product.sku == "ABC123"

def test_get_invalid_product(db):
    with pytest.raises(Exception):
        get_product(db, "12345")

def test_search_products(db):
    results = search_products(db, category="categ1", name="test1")
    assert len(results) == 1
    assert results[0].sku == "ABC123"

def test_invalid_search_products(db):
    with pytest.raises(Exception):
        search_products(db, category="12345", name="12345")

def test_update_product(db, updated_product):
    updated = update_product(db, "ABC123", updated_product)
    assert updated.name == "new name"
    assert updated.base_price == 500

def test_invalid_update_product(db, updated_product):
    with pytest.raises(Exception):
        update_product(db, "12345", updated_product)

def test_delete_product(db):
    delete_product(db, "ABC123")
    with pytest.raises(Exception):
        get_product(db, "ABC123")

def test_invalid_delete_product(db):
    with pytest.raises(Exception):
        delete_product(db, "12345")