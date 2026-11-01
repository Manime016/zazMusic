
from getpass import getpass

from sqlalchemy.exc import SQLAlchemyError

from server.config.database import SessionLocal, engine
from server.model.admin import Admin
from server.Utility.security import hash_password


def create_first_admin():
    # Ensure the admins table exists.
    Admin.__table__.create(bind=engine, checkfirst=True)

    db = SessionLocal()

    try:
        # Prevent accidental creation of another initial admin.
        existing_admin = db.query(Admin).first()

        if existing_admin:
            print("An admin already exists.")
            print("Initial admin setup is not allowed again.")
            return

        print("\n=== ZazMusic First Admin Setup ===\n")

        username = input("Enter admin username: ").strip()
        email = input("Enter admin email: ").strip().lower()

        if len(username) < 3:
            print("Username must contain at least 3 characters.")
            return

        if not email or "@" not in email:
            print("Enter a valid email address.")
            return

        password = getpass("Enter admin password: ")
        confirm_password = getpass("Confirm admin password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        admin = Admin(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("\nFirst admin created successfully!")
        print(f"Admin ID: {admin.id}")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")

    except SQLAlchemyError as error:
        db.rollback()
        print(f"Database error: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    create_first_admin()
