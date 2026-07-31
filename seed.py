from app.database import SessionLocal
from app.models.user import User
from app.auth import get_password_hash

db = SessionLocal()

# Check if admin already exists
existing = db.query(User).filter(User.username == "admin").first()

if existing:
    print("Admin already exists.")
else:
    admin = User(
        username="admin",
        password=get_password_hash("admin123"),
        role="admin"
    )

    db.add(admin)
    db.commit()

    print("Admin user created successfully!")

db.close()