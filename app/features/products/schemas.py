from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock: int = 0


class ProductRead(ProductBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
