from fastapi import APIRouter

from app.features.orders.schemas import OrderBase
from app.features.orders.service import create_order, get_order, list_orders

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"module": "orders", "status": "ready"}


@router.get("/")
def read_orders() -> list[dict]:
    return list_orders()


@router.get("/{order_id}")
def read_order(order_id: int) -> dict | None:
    return get_order(order_id)


@router.post("/")
def add_order(payload: OrderBase) -> dict:
    return create_order(payload)
