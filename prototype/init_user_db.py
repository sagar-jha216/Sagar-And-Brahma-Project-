from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, User, get_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize database with default admin user"""
    
    # Database setup
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shrink_sense.db")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            # Create default admin user
            hashed_password = get_password_hash("admin")
            admin_user = User(
                username="admin",
                email="admin@shrinksense.com",
                hashed_password=hashed_password,
                full_name="System Administrator",
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created (username: admin, password: admin)")
        else:
            print("ℹ️  Admin user already exists")
        
        # Create a sample regular user
        regular_user = db.query(User).filter(User.username == "user").first()
        if not regular_user:
            hashed_password = get_password_hash("password123")
            regular_user = User(
                username="user",
                email="user@shrinksense.com",
                hashed_password=hashed_password,
                full_name="Regular User",
                is_admin=False,
                is_active=True
            )
            db.add(regular_user)
            db.commit()
            print("✅ Sample regular user created (username: user, password: password123)")
        else:
            print("ℹ️  Regular user already exists")
            
        print("\n📊 Database initialized successfully!")
        print("🌐 You can now start the API server with: uvicorn main:app --reload")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
