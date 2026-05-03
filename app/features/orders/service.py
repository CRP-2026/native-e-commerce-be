from app.features.orders.schemas import OrderBase


def list_orders() -> list[dict]:
    return []


def get_order(order_id: int) -> dict | None:
    _ = order_id
    return None


def create_order(payload: OrderBase) -> dict:
    return payload.model_dump()
