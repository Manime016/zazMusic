from config.database import Base, engine
from model.user import User
from dotenv import load_dotenv

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")