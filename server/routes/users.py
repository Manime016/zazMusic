
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.config.database import get_db
from server.dependencies.auth import get_current_regular_user
from server.schema.user import UserCreate, UserLogin, UserResponse
from server.services.auth_service import register_user, login_user


router = APIRouter(tags=["Users"])


@router.post(
    "/create_account",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    credentials: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(credentials, db)


@router.post("/login")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user(credentials, db)


@router.get(
    "/users/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: dict = Depends(get_current_regular_user),
):
    return current_user
