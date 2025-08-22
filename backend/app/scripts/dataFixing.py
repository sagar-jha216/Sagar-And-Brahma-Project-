from sqlalchemy import create_engine, text

def add_is_admin_column():
    engine = create_engine("sqlite:///./shrink_sense.db")  # Adjust path if needed
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE user ADD COLUMN isAdmin BOOLEAN DEFAULT 0"))
