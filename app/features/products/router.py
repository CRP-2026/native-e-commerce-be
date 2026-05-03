from fastapi import APIRouter

from app.features.products.schemas import ProductBase
from app.features.products.service import create_product, get_product, list_products

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"module": "products", "status": "ready"}


@router.get("/")
def read_products() -> list[dict]:
    return list_products()


@router.get("/{product_id}")
def read_product(product_id: int) -> dict | None:
    return get_product(product_id)


@router.post("/")
def add_product(payload: ProductBase) -> dict:
    return create_product(payload)
