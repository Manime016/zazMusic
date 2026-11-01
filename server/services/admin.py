from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from server.model.admin import Admin
from server.schema.admin import AdminCreate, AdminLogin
from server.Utility.security import (
    hash_password,
    verify_password,
    create_access_token
)

def register_admin(
    credentials: AdminCreate,
    db: Session
):
    # 1. Check whether email already exists
    existing_admin = db.query(Admin).filter(
        Admin.email == credentials.email
    ).first()

    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # 2. Hash password
    hashed_password = hash_password(
        credentials.password
    )

    # 3. Create new admin
    new_admin = Admin(
        username=credentials.username,
        email=str(credentials.email),
        password_hash=hashed_password
    )

    # 4. Save admin to database
    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

    except Exception:
        db.rollback()
        raise

    return new_admin

def login_admin(
    credentials: AdminLogin,
    db: Session
):
    # 1. Find admin using email
    admin = db.query(Admin).filter(
        Admin.email == credentials.email
    ).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 2. Verify password
    if not verify_password(
        credentials.password,
        admin.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Create access token
    access_token = create_access_token(
        data={"sub": str(admin.id)}
    )

    return {"access_token": access_token, "token_type": "bearer"}