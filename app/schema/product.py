from pydantic import BaseModel,Field,ConfigDict

from datetime import datetime

from decimal import Decimal



class ProductCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150
    )

    description: str | None  = None

    price: Decimal = Field(
        gt=0
    )

    stock: int = Field(
        gt=0
    )


class ProductResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    active: bool
    created_at: datetime
    updated_at: datetime



class ProductUpdate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150
    )
    description: str | None  = None
    price: Decimal = Field(gt=0)
    stock: int = Field(gt=0)
    active: bool


class ProductPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, gt=0)
    active: bool | None = None