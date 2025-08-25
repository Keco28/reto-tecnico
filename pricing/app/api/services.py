import logging
from fastapi import HTTPException
from app.database import schemas
import requests
import os
from dotenv import load_dotenv
from app.database.tables import TAX_BY_COUNTRY, COUPONS

load_dotenv()

CATALOG_URL = os.getenv("CATALOG_URL")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_pricing(pricing_quote: schemas.PricingBase):

##Solicitud al servicio de catálogo
    try:
        response = requests.get(f"{CATALOG_URL}/products/{pricing_quote.product_sku}", timeout=5)
        if response.status_code == 404:
            logger.error(f"Product with SKU ({pricing_quote.product_sku}): {response.status_code} {response.text}")
            raise HTTPException(status_code=404, detail="Not Found")
        fetched_product = response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Request timed out")
        raise HTTPException(status_code=504, detail="Catalog service timeout")
    except requests.RequestException as e:
        logger.error(f"Error fetching product: {e}")
        raise HTTPException(status_code=503, detail="Catalog service unavailable")

    base_price = fetched_product["base_price"]
    logger.info(f"Creating pricing: {pricing_quote}")

    discount = COUPONS[pricing_quote.coupon] if pricing_quote.coupon else 0.0
    tax = TAX_BY_COUNTRY[pricing_quote.country]

    price_after_discount = base_price * (1 - discount)
    final_price = price_after_discount * (1 + tax)

    return schemas.PricingResponse(
        product_sku=pricing_quote.product_sku,
        base_price=base_price,
        final_price=final_price,
        currency=fetched_product["currency"],
        total_discounted=base_price - price_after_discount,
        total_taxed=final_price - price_after_discount
    )
