from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.databases.connection import get_db
from app.models.user import User
from app.schema.user import UserCreate, UserResponse
from app.security.password import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user_data: UserCreate,db: Session = Depends(get_db)
):
    # Comprobar si el correo ya existe
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado / Email already registered"
        )

    now = datetime.now(timezone.utc)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="customer",
        created_at=now,
        updated_at=now
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user