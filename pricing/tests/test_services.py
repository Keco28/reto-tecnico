import pytest
from typing import Any
from unittest.mock import patch, MagicMock
from app.api import services
from app.database import schemas
from fastapi import HTTPException


class DummyPricingBase:
	def __init__(self, product_sku, country, coupon=None):
		self.product_sku = product_sku
		self.country = country
		self.coupon = coupon

def mock_setup(status_code: int, json_data: Any):
	mock_response = MagicMock()
	mock_response.status_code = status_code
	mock_response.json.return_value = json_data
	if status_code == 404:
		mock_response.raise_for_status.side_effect = HTTPException(status_code=404, detail="Not Found")
	return mock_response

def test_create_pricing():
	pricing_quote = DummyPricingBase(product_sku="ABC123", coupon="BANCOLMARTES", country="CO")
	mock_product = {"product_sku": "ABC123","base_price": 200,"final_price": 214.2,"currency": "COP","total_discounted": 20,"total_taxed": 34.19999999999999}
	with patch("app.api.services.requests.get") as mock_get:
		mock_get.return_value = mock_setup(200, mock_product)
		with patch("app.api.services.CATALOG_URL", "http://fake-url.com"):
			result = services.create_pricing(pricing_quote)
			assert result.base_price == 200
			assert result.final_price == pytest.approx(200 * (1 - 0.1) * (1 + 0.19))
			assert result.currency == "COP"
			assert result.total_discounted == pytest.approx(200 * 0.1)
			assert result.total_taxed == pytest.approx(200 * (1 - 0.1) * 0.19)

def test_create_pricing_no_coupon():
	pricing_quote = DummyPricingBase(product_sku="ABC123", country="CO")
	mock_product = {"product_sku": "ABC123","base_price": 200,"final_price": 238,"currency": "COP","total_discounted": 0,"total_taxed": 38}
	with patch("app.api.services.requests.get") as mock_get:
		mock_get.return_value = mock_setup(200, mock_product)
		with patch("app.api.services.CATALOG_URL", "http://fake-url.com"):
			result = services.create_pricing(pricing_quote)
			assert result.final_price == pytest.approx(200 * (1 + 0.19))
			assert result.total_discounted == 0
			assert result.total_taxed == pytest.approx(200 * 0.19)

def test_invalid_sku_create_pricing():
	pricing_quote = DummyPricingBase(product_sku="12345", country="CO")
	mock_product = {"detail": "Not Found"}
	with patch("app.api.services.requests.get") as mock_get:
		mock_get.return_value = mock_setup(404, mock_product)
		with patch("app.api.services.CATALOG_URL", "http://fake-url.com"):
			with pytest.raises(HTTPException) as excinfo:
				services.create_pricing(pricing_quote)
			assert excinfo.value.status_code == 404

def test_create_pricing_catalog_timeout():
	pricing_quote = DummyPricingBase(product_sku="ABC123", coupon="BANCOLMARTES", country="CO")
	with patch("app.api.services.requests.get", side_effect=services.requests.exceptions.Timeout()):
		with patch("app.api.services.CATALOG_URL", "http://fake-url.com"):
			with pytest.raises(HTTPException) as excinfo:
				services.create_pricing(pricing_quote)
			assert excinfo.value.status_code == 504

def test_create_pricing_catalog_unavailable():
	pricing_quote = DummyPricingBase(product_sku="ABC123", coupon="BANCOLMARTES", country="CO")
	with patch("app.api.services.requests.get", side_effect=services.requests.RequestException()):
		with patch("app.api.services.CATALOG_URL", "http://fake-url.com"):
			with pytest.raises(HTTPException) as excinfo:
				services.create_pricing(pricing_quote)
			assert excinfo.value.status_code == 503
