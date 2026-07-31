import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Local database ke liye fallback
LOCAL_DATABASE_URL = "postgresql://postgres:rakhi%402005@localhost:1220/clinic_db"


# Deployment (Render) par DATABASE_URL use hoga
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    LOCAL_DATABASE_URL
)


# Render PostgreSQL me kabhi-kabhi postgres:// aata hai
# SQLAlchemy ko postgresql:// chahiye hota hai
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()