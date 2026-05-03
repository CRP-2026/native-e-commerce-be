from app.features.products.schemas import ProductBase


def list_products() -> list[dict]:
    return []


def get_product(product_id: int) -> dict | None:
    _ = product_id
    return None


def create_product(payload: ProductBase) -> dict:
    return payload.model_dump()
