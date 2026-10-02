from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.Base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order_item import OrderItem


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None
    )

    price: Mapped[Numeric] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )

    active: Mapped[Boolean] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product"
    )


