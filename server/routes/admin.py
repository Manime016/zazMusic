
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.config.database import get_db
from server.dependencies.auth import get_current_admin
from server.schema.admin import AdminCreate, AdminLogin, AdminResponse
from server.services.admin import register_admin, login_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/create_account",
    response_model=AdminResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    credentials: AdminCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return register_admin(credentials, db)


@router.post("/login")
def login(
    credentials: AdminLogin,
    db: Session = Depends(get_db),
):
    return login_admin(credentials, db)
