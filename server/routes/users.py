from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.config.database import get_db
from server.schema.user import (
    UserCreate,
    UserLogin,
    UserResponse
)
from server.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter()


# USER REGISTRATION
@router.post(
    "/create_account",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_account(
    credentials: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = register_user(credentials, db)

    return new_user


# USER LOGIN
@router.post("/login")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(credentials, db)
