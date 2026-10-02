from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.databases.Base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order

 

class User(Base):
    __tablename__ = "users"


    id : Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True

    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False

    )

    role: Mapped[str] = mapped_column(
            String(50),
            nullable=False,
            default="customer"
            
        )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user"

    )

    



    