
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from server.model.admin import Admin
from server.schema.admin import AdminCreate, AdminLogin
from server.Utility.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def register_admin(credentials: AdminCreate, db: Session):
    existing_admin = (
        db.query(Admin)
        .filter(Admin.email == str(credentials.email))
        .first()
    )

    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin email already registered",
        )

    new_admin = Admin(
        username=credentials.username,
        email=str(credentials.email),
        password_hash=hash_password(credentials.password),
    )

    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
    except Exception:
        db.rollback()
        raise

    return new_admin


def login_admin(credentials: AdminLogin, db: Session):
    admin = (
        db.query(Admin)
        .filter(Admin.email == str(credentials.email))
        .first()
    )

    if not admin or not verify_password(
        credentials.password,
        admin.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=admin.id,
        role="admin",
    )

    return {
        "message": "Admin login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "admin": {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
        },
    }
