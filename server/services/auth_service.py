
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from server.model.user import User
from server.schema.user import UserCreate, UserLogin
from server.Utility.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(
    credentials: UserCreate,
    db: Session
):
    # 1. Check whether email already exists
    existing_user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # 2. Hash password
    hashed_password = hash_password(
        credentials.password
    )

    # 3. Create new user
    new_user = User(
        username=credentials.username,
        email=str(credentials.email),
        password_hash=hashed_password
    )

    # 4. Save user to database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()
        raise

    return new_user


def login_user(
    credentials: UserLogin,
    db: Session
):
    # 1. Find user using email
    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    # 2. Check whether user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Verify password
    if not verify_password(
        credentials.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 4. Generate JWT token
    access_token = create_access_token(user.id)

    # 5. Return login result
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }
