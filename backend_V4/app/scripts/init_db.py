from app.database import engine
from app.models import Base  # imports models and Base

def init():
    Base.metadata.create_all(bind=engine)
    print("Database and tables created.")

if __name__ == "__main__":
    init()
