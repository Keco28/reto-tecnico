import pytest
from app.database.schemas import PricingBase

def test_pricing_base_model():
    quote = PricingBase(
        product_sku="ABC123",
        coupon="BANCOLMARTES",
        country="CO"
    )
    assert quote.country=="CO"
    assert quote.coupon=="BANCOLMARTES"

def test_invalid_pricing_base_model():
    with pytest.raises(ValueError, match="Field required"):
        PricingBase(
            coupon="BANCOLMARTES",
            country="CO"
        )

def test_invalid_coupon():
    invalid_coupon = "BANQUITO"
    with pytest.raises(ValueError, match=f"coupon '{invalid_coupon}' is not valid"):
        PricingBase(
            product_sku="ABC123",
            coupon=invalid_coupon,
            country="CO"
        )
        
def test_invalid_country():
    invalid_country = "XX"
    with pytest.raises(ValueError, match=f"country '{invalid_country}' is not valid"):
        PricingBase(
            product_sku="ABC123",
            coupon="BANCOLMARTES",
            country=invalid_country
        )
        
