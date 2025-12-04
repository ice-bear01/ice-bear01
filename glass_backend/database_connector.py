from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "postgresql+psycopg2://jjj:jjj2025@localhost:8080/jjj"
# DATABASE_URL = "postgresql+psycopg2://glass:vkn40zprjpvUona4837eOfD5Vkclp0at@dpg-d3q16uggjchc73avtcq0-a.oregon-postgres.render.com:5432/glass_database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
