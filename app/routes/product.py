# GET /products → traer productos desde PostgreSQL.
# POST /products → crear productos.
# GET /products/{id} → buscar un producto específico.
# PUT/PATCH → actualizar.
# DELETE → eliminar/desactivar.
# Finalmente POST /orders → aquí entra toda la lógica importante de Orden + OrdenItem + Product + stock + total.
# Generar el ticket de la orden.

from datetime import datetime, timezone

from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.databases.connection import get_db
from app.models.product import Product
from app.schema.product import ProductCreate,ProductPatch,ProductResponse, ProductUpdate



router = APIRouter(
    prefix="/product",
    tags=["Product"]
)


# GET /products → traer productos desde PostgreSQL.
@router.get("/", response_model=list[ProductResponse])
def products_db(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.active.is_(True)).all()
    return products


# POST /products → crear productos.
@router.post("/", response_model=ProductResponse)
def crear_products(product: ProductCreate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        active=True,
        created_at=now,
        updated_at=now,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# GET /products/{id} → buscar un producto específico.

@router.get("/{product_id}",response_model=ProductResponse)
def product_id(product_id : int, db:Session = Depends(get_db)):

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.active.is_(True)

    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado / Product not found"
        )
    return product




# PUT/PATCH → actualizar.
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    db_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if db_product is None:
        raise HTTPException(status_code=404,detail="Producto no encontrado / Product not found")

    db_product.name = product_update.name
    db_product.price = product_update.price
    db_product.description = product_update.description
    db_product.stock = product_update.stock
    db_product.active = product_update.active
    db_product.updated_at = now

    db.commit()
    db.refresh(db_product)
    return db_product


@router.patch("/{product_id}", response_model=ProductResponse)
def oneUdapteProduct(product_id: int, product_one_update: ProductPatch, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    db_product = db.query(Product).filter(Product.id == product_id).first()

    if db_product is None:
        raise HTTPException(status_code=404,detail="Producto no encontrado / Product not found")

    update_values = product_one_update.model_dump(exclude_unset=True)

    for field, value in update_values.items():
        setattr(db_product, field, value)

    db_product.updated_at = now

    db.commit()
    db.refresh(db_product)

    return db_product
    

# DELETE → eliminar/desactivar.

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product( product_id: int, db: Session = Depends(get_db)):
    
    db_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado / Product not found"
        )

    db_product.active = False
    db_product.updated_at = datetime.now(timezone.utc)

    db.commit()

    return None

        






