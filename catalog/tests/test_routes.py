import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_request():
    response = client.get("/products/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_product_request():
    response = client.get("/products/ABC123")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "sku": "ABC123", "name": "test1", "description": "desc1", "base_price": 200, "currency": "COP", "category": "categ1"}

def test_get_invalid_product_request():
    response = client.get("/products/123456")
    assert response.status_code == 404

def test_search_products_request():
    response = client.get("/products?category=categ1&name=test1&min_price=1&max_price=250")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_invalid_search_products_request():
    response = client.get("/products?category=x&name=y&min_price=1&max_price=1")
    assert response.status_code == 404

def test_create_product_request(request_data):
    response = client.post("/products/", json=request_data)
    assert response.status_code == 201
    assert response.json() == {"id": 2, "sku": "DEF4563", "name": "test2", "description": "desc2", "base_price": 3200, "currency": "USD", "category": "categ2"}

def test_invalid_create_product_request(request_data):
    request_data["base_price"] = -100
    response = client.post("/products/", json=request_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, base_price must be greater than 0"

def test_invalid_create_missing_product_request(request_data):
    request_data.pop("category")
    response = client.post("/products/", json=request_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_update_product_request():
    response = client.put("/products/ABC123", json={
        "description": "desc1_updated",
        "base_price": 3500,
        "currency": "USD"
    })
    assert response.status_code == 200
    assert response.json() == {"id": 1, "sku": "ABC123", "name": "test1", "description": "desc1_updated", "base_price": 3500, "currency": "USD", "category": "categ1"}
    
def test_invalid_update_product_request():
    response = client.put("/products/ABC123", json={
        "base_price": -1
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, base_price must be greater than 0"
    
def test_delete_product_request():
    response = client.delete("/products/ABC123")
    assert response.status_code == 204

def test_invalid_delete_product_request():
    response = client.delete("/products/123456")
    assert response.status_code == 404