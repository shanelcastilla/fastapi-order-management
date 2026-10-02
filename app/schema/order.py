from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime

from decimal import Decimal

from app.schema.order_item import OrderItemCreate, OrderItemResponse


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate] = Field(
        min_length=1
    )


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int = Field(validation_alias="id_user")
    status: str
    total: Decimal
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

   