import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Flexible database path for Azure (e.g. /home/site/wwwroot/recipes.db)
db_path = os.getenv("DATABASE_PATH", "/home/site/wwwroot/recipes.db")
DATABASE_URL = f"sqlite:///{os.path.abspath(db_path)}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class RecipeDB(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients_list = Column(Text) # JSON string array
    instructions = Column(Text) # JSON string array
    cook_time = Column(String)
    nutrition = Column(Text) # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
