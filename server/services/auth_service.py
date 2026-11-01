
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from server.model.user import User
from server.schema.user import UserCreate, UserLogin
from server.Utility.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def register_user(credentials: UserCreate, db: Session):
    existing_user = (
        db.query(User)
        .filter(User.email == str(credentials.email))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    new_user = User(
        username=credentials.username,
        email=str(credentials.email),
        password_hash=hash_password(credentials.password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    return new_user


def login_user(credentials: UserLogin, db: Session):
    user = (
        db.query(User)
        .filter(User.email == str(credentials.email))
        .first()
    )

    if not user or not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=user.id,
        role="user",
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }
