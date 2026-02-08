# Connexion 
from app.core.config import db_url 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Annotated
from fastapi import Depends

# engine
engine = create_engine(db_url)

# session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base
Base = declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy=Annotated[Session, Depends(get_db)]
