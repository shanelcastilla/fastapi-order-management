from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.databases.connection import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User

from app.schema.order import OrderCreate, OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):

    # 1. Comprobar que existe el usuario
    user = db.query(User).filter(
        User.id == order_data.user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado / User not found"
        )

    # 2. Variables para construir la orden
    total = Decimal("0")
    order_items = []
    requested_quantities = {}

    # 3. Revisar cada producto solicitado
    for item in order_data.items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {item.product_id} no encontrado / Product {item.product_id} not found"
            )

        if not product.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto {product.id} no está disponible / Product {product.id} is not available"
            )

        requested_quantity = requested_quantities.get(product.id, 0) + item.quantity

        if product.stock < requested_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {product.id} / Insufficient stock for product {product.id}"
            )

        requested_quantities[product.id] = requested_quantity

        # 4. Calcular subtotal
        subtotal = product.price * item.quantity

        total += subtotal

        # 5. Preparar OrderItem
        order_items.append({
            "product": product,
            "quantity": item.quantity,
            "unit_price": product.price,
            "subtotal": subtotal
        })

    # 6. Crear la orden
    now = datetime.now(timezone.utc)

    new_order = Order(
        id_user=order_data.user_id,
        status="pending",
        total=total,
        created_at=now,
        updated_at=now
    )

    db.add(new_order)
    db.flush()

    # 7. Crear los OrderItems y descontar stock
    for item in order_items:

        product = item["product"]

        new_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=item["subtotal"]
        )

        db.add(new_item)

        product.stock -= item["quantity"]

    # 8. Guardar todos los cambios
    db.commit()

    # 9. Actualizar la orden
    db.refresh(new_order)

    return new_order