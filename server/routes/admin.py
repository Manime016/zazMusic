from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.config.database import get_db

from server.schema.admin import (
    AdminCreate,
    AdminLogin,
    AdminResponse
)
from server.services.admin import (
    register_admin,
    login_admin
)
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post(
    "/create_account",
    response_model=AdminResponse
)
def create_account(
    credentials: AdminCreate,
    db: Session = Depends(get_db)
):
    new_admin = register_admin(credentials, db)

    return new_admin

@router.post("/login", response_model=AdminResponse)
def login(
    credentials: AdminLogin,
    db: Session = Depends(get_db)
):
    return login_admin(credentials, db)

