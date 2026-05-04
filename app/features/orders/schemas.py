from decimal import Decimal

from pydantic import BaseModel, Field


class OrderLineIn(BaseModel):
    product_id: str = Field(alias="productId")
    variant_id: str | None = Field(default=None, alias="variantId")
    quantity: int = Field(ge=1)

    model_config = {"populate_by_name": True}


class OrderCreateIn(BaseModel):
    items: list[OrderLineIn] = Field(min_length=1)
    shipping_address_id: str = Field(alias="shippingAddressId")
    payment_method_code: str = Field(alias="paymentMethod")
    shipping_fee: Decimal = Field(default=Decimal("0"), alias="shippingFee")
    discount_total: Decimal = Field(default=Decimal("0"), alias="discountTotal")

    model_config = {"populate_by_name": True}
