from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    status: str = "pending"
    total_amount: Decimal = Decimal("0.00")


class OrderRead(OrderBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
