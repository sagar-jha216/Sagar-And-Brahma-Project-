# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.schemas.user import UserCreate
# from app.controllers.user import create_user

# def seed_users():
#     db: Session = SessionLocal()

#     try:
#         for i in range(1, 11):
#             username = f"user{i}"
#             password = f"user{i}"
#             user_data = UserCreate(userName=username, password=password, isAdmin=False)

#             # Check if user already exists to avoid duplicates
#             existing_user = db.query(create_user.__annotations__['return']).filter_by(userName=username).first()
#             if not existing_user:
#                 created_user = create_user(user_data, db)
#                 print(f"✅ Created: {created_user.userName}")
#             else:
#                 print(f"⚠️ Skipped (already exists): {username}")
#     finally:
#         db.close()

# if __name__ == "__main__":
#     seed_users()
