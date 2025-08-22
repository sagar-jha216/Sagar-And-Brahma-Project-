from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import get_password_hash

def seed():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        print("Admin already exists")
        return
    u = User(username="admin", full_name="Admin", hashed_password=get_password_hash("admin123"))
    db.add(u)
    db.commit()
    print("Created admin user (username=admin, password=admin123)")

if __name__ == "__main__":
    seed()