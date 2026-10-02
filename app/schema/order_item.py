from pydantic import BaseModel, Field, ConfigDict

from decimal import Decimal


class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(
        gt=0
    )


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal