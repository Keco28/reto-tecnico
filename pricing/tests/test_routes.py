import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

request_data = {
        "product_sku": "ABC123",
        "coupon": "BANCOLMARTES",
        "country": "CO"
    }

def test_health_check_request():
    response = client.get("/pricing/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
def test_invalid_sku_create_pricing_quote_request():
    data = request_data.copy()
    data["product_sku"] = "12345"
    response = client.post("/pricing/quote", json=data)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Not Found"

def test_invalid_coupon_create_pricing_quote_request():
    data = request_data.copy()
    data["coupon"] = "BANQUITO"
    response = client.post("/pricing/quote", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == f"Value error, coupon '{data['coupon']}' is not valid"

def test_invalid_country_create_pricing_quote_request():
    data = request_data.copy()
    data["country"] = "XX"
    response = client.post("/pricing/quote", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == f"Value error, country '{data['country']}' is not valid"