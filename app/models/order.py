from sqlalchemy import String, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.Base import Base

from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.order_item import OrderItem


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    id_user: Mapped[int] = mapped_column(
        "user_id",
        ForeignKey("users.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending"
    )

    total: Mapped[Numeric] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(nullable=False)

    updated_at: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="orders")

    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")











